# /usr/bin/env python3
# Alpha Vantage API Client
# Handles API requests, response parsing, and error handling

import os
import time
import requests
import pandas as pd
from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from dotenv import load_dotenv
from src.cache_manager import CacheManager


# API Configuration
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"
API_TIMEOUT = 30  # seconds
MAX_API_RETRIES = 3
RETRY_BACKOFF_FACTOR = 2  # exponential backoff
DEFAULT_OUTPUT_SIZE = "full"


# Custom Exceptions
class APIError(Exception):
    """Base exception for API-related errors."""

    pass


class RateLimitError(APIError):
    """Raised when API rate limit is exceeded."""

    pass


class InvalidSymbolError(APIError):
    """Raised when stock symbol is not found."""

    pass


class NetworkError(APIError):
    """Raised when network request fails."""

    pass


# Response key mappings for different time series functions
TIME_SERIES_KEYS = {
    "TIME_SERIES_DAILY": "Time Series (Daily)",
    "TIME_SERIES_DAILY_ADJUSTED": "Time Series (Daily)",
    "TIME_SERIES_WEEKLY": "Weekly Time Series",
    "TIME_SERIES_WEEKLY_ADJUSTED": "Weekly Adjusted Time Series",
    "TIME_SERIES_MONTHLY": "Monthly Time Series",
    "TIME_SERIES_MONTHLY_ADJUSTED": "Monthly Adjusted Time Series",
    "TIME_SERIES_INTRADAY": None,  # Will be determined dynamically
}


class AlphaVantageClient:
    """
    Client for Alpha Vantage API with caching and error handling.

    Features:
    - Automatic caching of responses
    - Network error retry with exponential backoff
    - Rate limit detection
    - Invalid symbol detection
    - Response validation
    - DataFrame conversion with proper typing
    """

    def __init__(self, api_key: Optional[str] = None, use_cache: bool = True):
        """
        Initialize Alpha Vantage API client.

        Args:
            api_key: Alpha Vantage API key (defaults to environment variable)
            use_cache: Whether to use caching (default True)
        """
        # Load environment variables
        load_dotenv()

        # Get API key
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")
        if not self.api_key or self.api_key == "your_api_key_here":
            raise APIError("Alpha Vantage API key not configured")

        self.base_url = ALPHA_VANTAGE_BASE_URL
        self.use_cache = use_cache
        self.cache_manager = CacheManager() if use_cache else None

    def _make_request(self, params: Dict[str, str], retry_count: int = 0) -> Dict[str, Any]:
        """
        Make HTTP request to Alpha Vantage API with retry logic.

        Args:
            params: Query parameters for API request
            retry_count: Current retry attempt

        Returns:
            Parsed JSON response

        Raises:
            NetworkError: If request fails after retries
            RateLimitError: If API rate limit exceeded
            InvalidSymbolError: If symbol not found
        """
        # Add API key to parameters
        params["apikey"] = self.api_key

        try:
            response = requests.get(self.base_url, params=params, timeout=API_TIMEOUT)
            response.raise_for_status()

            data = response.json()

            # Check for API error messages
            if "Error Message" in data:
                raise InvalidSymbolError(f"Invalid symbol: {data['Error Message']}")

            if "Note" in data:
                # Rate limit message
                raise RateLimitError(
                    "API rate limit reached (25 requests per day). "
                    "Try again tomorrow or use cached data."
                )

            if "Information" in data and "rate limit" in data["Information"].lower():
                raise RateLimitError("API rate limit reached. " f"Details: {data['Information']}")

            return data

        except requests.exceptions.Timeout:
            if retry_count < MAX_API_RETRIES:
                wait_time = RETRY_BACKOFF_FACTOR**retry_count
                print(
                    f"Request timeout. Retrying in {wait_time} seconds... (attempt {retry_count + 1}/{MAX_API_RETRIES})"
                )
                time.sleep(wait_time)
                return self._make_request(params, retry_count + 1)
            raise NetworkError("Request timeout after multiple retries")

        except requests.exceptions.ConnectionError:
            if retry_count < MAX_API_RETRIES:
                wait_time = RETRY_BACKOFF_FACTOR**retry_count
                print(
                    f"Connection error. Retrying in {wait_time} seconds... (attempt {retry_count + 1}/{MAX_API_RETRIES})"
                )
                time.sleep(wait_time)
                return self._make_request(params, retry_count + 1)
            raise NetworkError("Connection error after multiple retries")

        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Request failed: {str(e)}")

    def _parse_time_series_data(self, data: Dict[str, Any], function: str) -> pd.DataFrame:
        """
        Parse Alpha Vantage time series response into pandas DataFrame.

        Args:
            data: API response JSON
            function: Time series function name

        Returns:
            pandas DataFrame with datetime index

        Raises:
            APIError: If response format is invalid
        """
        # Determine the correct time series key
        if function == "TIME_SERIES_INTRADAY":
            # Find the time series key dynamically for intraday
            time_series_key = None
            for key in data.keys():
                if key.startswith("Time Series"):
                    time_series_key = key
                    break
        else:
            time_series_key = TIME_SERIES_KEYS.get(function)

        if not time_series_key or time_series_key not in data:
            raise APIError(f"Unexpected API response format. Expected key: {time_series_key}")

        time_series_data = data[time_series_key]

        if not time_series_data:
            raise APIError("No time series data in API response")

        # Convert to DataFrame
        df = pd.DataFrame.from_dict(time_series_data, orient="index")

        # Convert index to datetime
        df.index = pd.to_datetime(df.index)
        df.index.name = "Date"

        # Sort by date (oldest to newest)
        df.sort_index(inplace=True)

        # Rename columns (remove number prefixes like "1. open")
        column_mapping = {}
        for col in df.columns:
            # Extract the name after the number and period
            if ". " in col:
                clean_name = col.split(". ")[1]
                # Capitalize first letter
                clean_name = clean_name.capitalize()
                column_mapping[col] = clean_name
            else:
                column_mapping[col] = col

        df.rename(columns=column_mapping, inplace=True)

        # Convert all columns to float
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        return df

    def fetch_stock_data(
        self,
        symbol: str,
        function: str,
        interval: Optional[str] = None,
        outputsize: str = DEFAULT_OUTPUT_SIZE,
    ) -> pd.DataFrame:
        """
        Fetch stock data from Alpha Vantage API with caching.

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')
            function: Time series function (e.g., 'TIME_SERIES_DAILY')
            interval: Intraday interval (required for TIME_SERIES_INTRADAY)
            outputsize: 'compact' (100 points) or 'full' (all available)

        Returns:
            pandas DataFrame with stock data

        Raises:
            APIError: If API request or parsing fails
            RateLimitError: If rate limit exceeded
            InvalidSymbolError: If symbol not found
            NetworkError: If network request fails
        """
        # Validate inputs
        symbol = symbol.upper().strip()

        if function == "TIME_SERIES_INTRADAY" and not interval:
            raise APIError("Interval required for TIME_SERIES_INTRADAY")

        # Check cache first
        if self.use_cache:
            cached_data = self.cache_manager.get_cached_data(symbol, function, interval, outputsize)
            if cached_data is not None:
                print(f"Using cached data for {symbol} ({function})")
                return cached_data

        # Build request parameters
        params = {"function": function, "symbol": symbol, "outputsize": outputsize}

        # Add interval for intraday
        if interval:
            params["interval"] = interval

        print(f"Fetching {function} data for {symbol}...")

        # Make API request
        response_data = self._make_request(params)

        # Parse response
        df = self._parse_time_series_data(response_data, function)

        # Cache the result
        if self.use_cache:
            self.cache_manager.save_to_cache(df, symbol, function, interval, outputsize)
            print(f"Data cached for future use")

        return df

    def get_daily(
        self, symbol: str, adjusted: bool = False, outputsize: str = DEFAULT_OUTPUT_SIZE
    ) -> pd.DataFrame:
        """
        Get daily time series data.

        Args:
            symbol: Stock ticker symbol
            adjusted: Whether to use adjusted prices
            outputsize: 'compact' or 'full'

        Returns:
            pandas DataFrame with daily data
        """
        function = "TIME_SERIES_DAILY_ADJUSTED" if adjusted else "TIME_SERIES_DAILY"
        return self.fetch_stock_data(symbol, function, outputsize=outputsize)

    def get_weekly(self, symbol: str, adjusted: bool = False) -> pd.DataFrame:
        """
        Get weekly time series data.

        Args:
            symbol: Stock ticker symbol
            adjusted: Whether to use adjusted prices

        Returns:
            pandas DataFrame with weekly data
        """
        function = "TIME_SERIES_WEEKLY_ADJUSTED" if adjusted else "TIME_SERIES_WEEKLY"
        return self.fetch_stock_data(symbol, function)

    def get_monthly(self, symbol: str, adjusted: bool = False) -> pd.DataFrame:
        """
        Get monthly time series data.

        Args:
            symbol: Stock ticker symbol
            adjusted: Whether to use adjusted prices

        Returns:
            pandas DataFrame with monthly data
        """
        function = "TIME_SERIES_MONTHLY_ADJUSTED" if adjusted else "TIME_SERIES_MONTHLY"
        return self.fetch_stock_data(symbol, function)

    def get_intraday(
        self, symbol: str, interval: str = "5min", outputsize: str = DEFAULT_OUTPUT_SIZE
    ) -> pd.DataFrame:
        """
        Get intraday time series data.

        Args:
            symbol: Stock ticker symbol
            interval: Time interval ('1min', '5min', '15min', '30min', '60min')
            outputsize: 'compact' or 'full'

        Returns:
            pandas DataFrame with intraday data
        """
        return self.fetch_stock_data(symbol, "TIME_SERIES_INTRADAY", interval, outputsize)
