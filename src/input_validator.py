# /usr/bin/env python3
# Input Validation Utilities for Stock Data Visualization CLI
# Provides robust validation for user inputs with detailed error messages

import os
import re
from datetime import datetime, timedelta
from typing import Tuple, Optional
from dotenv import load_dotenv
from src.constants import (
    SYMBOL_MIN_LENGTH, SYMBOL_MAX_LENGTH,
    DATE_FORMAT, DATE_FORMAT_DISPLAY,
    MAX_DATE_RANGE_YEARS
)


class ValidationError(Exception):
    """Custom exception for validation errors with user-friendly messages."""
    pass


class EnvironmentValidator:
    """Validates environment configuration and API key setup."""

    @staticmethod
    def validate_env_file() -> bool:
        """
        Check if .env file exists and contains API key.

        Returns:
            bool: True if environment is properly configured

        Raises:
            ValidationError: If .env file is missing or API key is not configured
        """
        env_path = '.env'

        if not os.path.exists(env_path):
            raise ValidationError(
                "Configuration Error: .env file not found\n"
                "Please follow these steps:\n"
                "  1. Copy .env.example to .env: cp .env.example .env\n"
                "  2. Get your API key from: https://www.alphavantage.co/support/#api-key\n"
                "  3. Edit .env and add your API key: ALPHA_VANTAGE_API_KEY=your_key_here"
            )

        # Load environment variables
        load_dotenv()
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY', '').strip()

        if not api_key or api_key == 'your_api_key_here':
            raise ValidationError(
                "Configuration Error: API key not configured\n"
                "Please edit .env file and add your Alpha Vantage API key:\n"
                "  ALPHA_VANTAGE_API_KEY=your_actual_key_here\n"
                "Get your free API key from: https://www.alphavantage.co/support/#api-key"
            )

        return True


class StockSymbolValidator:
    """Validates stock ticker symbols."""

    @staticmethod
    def validate(symbol: str) -> str:
        """
        Validate stock symbol format and length.

        Args:
            symbol: Raw stock symbol input from user

        Returns:
            str: Validated and sanitized symbol in uppercase

        Raises:
            ValidationError: If symbol format is invalid
        """
        # Remove whitespace and convert to uppercase
        symbol = symbol.strip().upper()

        if not symbol:
            raise ValidationError("Stock symbol cannot be empty")

        # Check length constraints
        if len(symbol) < SYMBOL_MIN_LENGTH:
            raise ValidationError(
                f"Stock symbol too short (minimum {SYMBOL_MIN_LENGTH} character)\n"
                f"Examples: AAPL, MSFT, GOOGL, TSLA"
            )

        if len(symbol) > SYMBOL_MAX_LENGTH:
            raise ValidationError(
                f"Stock symbol too long (maximum {SYMBOL_MAX_LENGTH} characters)\n"
                f"Examples: AAPL, MSFT, GOOGL, TSLA"
            )

        # Validate format: only uppercase letters allowed
        if not re.match(r'^[A-Z]+$', symbol):
            raise ValidationError(
                "Stock symbol must contain only letters (no numbers or special characters)\n"
                f"Invalid: {symbol}\n"
                f"Valid examples: AAPL, MSFT, GOOGL, TSLA"
            )

        return symbol


class DateValidator:
    """Validates dates and date ranges for stock data queries."""

    @staticmethod
    def parse_date(date_str: str) -> Tuple[str, datetime]:
        """
        Parse and validate date string.

        Args:
            date_str: Date string in YYYY-MM-DD format

        Returns:
            Tuple of (validated date string, datetime object)

        Raises:
            ValidationError: If date format is invalid or date is in the future
        """
        date_str = date_str.strip()

        try:
            parsed_date = datetime.strptime(date_str, DATE_FORMAT)
        except ValueError:
            raise ValidationError(
                f"Invalid date format\n"
                f"Expected: {DATE_FORMAT_DISPLAY} (e.g., 2024-01-15)\n"
                f"Received: {date_str}"
            )

        # Check if date is in the future
        today = datetime.now()
        if parsed_date.date() > today.date():
            raise ValidationError(
                f"Date cannot be in the future\n"
                f"Specified: {date_str}\n"
                f"Today: {today.strftime(DATE_FORMAT)}"
            )

        return date_str, parsed_date

    @staticmethod
    def validate_date_range(begin_date: datetime, end_date: datetime,
                          begin_str: str, end_str: str) -> Tuple[str, str]:
        """
        Validate that date range is logical and reasonable.

        Args:
            begin_date: Starting date as datetime object
            end_date: Ending date as datetime object
            begin_str: Starting date as string (for error messages)
            end_str: Ending date as string (for error messages)

        Returns:
            Tuple of (begin_date_str, end_date_str) if valid

        Raises:
            ValidationError: If date range is invalid
        """
        # Check end date is after or equal to begin date
        if end_date < begin_date:
            raise ValidationError(
                f"End date must be on or after begin date\n"
                f"Begin: {begin_str}\n"
                f"End:   {end_str}"
            )

        # Check if date range is excessively large
        date_diff = end_date - begin_date
        years_diff = date_diff.days / 365.25

        if years_diff > MAX_DATE_RANGE_YEARS:
            raise ValidationError(
                f"Date range too large (maximum {MAX_DATE_RANGE_YEARS} years)\n"
                f"Requested range: {years_diff:.1f} years\n"
                f"Consider using weekly or monthly time series for large ranges"
            )

        # Warning for large daily ranges (informational, not blocking)
        if years_diff > 5 and date_diff.days > 1825:
            return begin_str, end_str, (
                f"Note: Large date range ({years_diff:.1f} years) may result in "
                f"slower API responses and large datasets"
            )

        return begin_str, end_str, None

    @staticmethod
    def check_weekend(date_obj: datetime) -> Optional[str]:
        """
        Check if date falls on a weekend (markets closed).

        Args:
            date_obj: Date to check

        Returns:
            Warning message if weekend, None otherwise
        """
        if date_obj.weekday() >= 5:  # Saturday = 5, Sunday = 6
            day_name = date_obj.strftime('%A')
            return f"Note: {date_obj.strftime(DATE_FORMAT)} is a {day_name} (market closed)"
        return None


class ChoiceValidator:
    """Validates menu choice selections."""

    @staticmethod
    def validate_choice(choice: str, valid_choices: dict, choice_type: str) -> str:
        """
        Validate that user choice matches one of the available options.

        Args:
            choice: User input choice
            valid_choices: Dictionary of valid choices (from constants)
            choice_type: Description of choice type (for error messages)

        Returns:
            str: The key from valid_choices dictionary

        Raises:
            ValidationError: If choice is not valid
        """
        choice = choice.strip()

        if not choice:
            raise ValidationError(f"{choice_type} cannot be empty")

        if choice not in valid_choices:
            valid_options = ', '.join(sorted(valid_choices.keys()))
            raise ValidationError(
                f"Invalid {choice_type.lower()}\n"
                f"Valid options: {valid_options}\n"
                f"Received: {choice}"
            )

        return choice


def format_error_message(error: Exception, retry_count: int, max_retries: int) -> str:
    """
    Format error message with retry information.

    Args:
        error: The exception that occurred
        retry_count: Current retry attempt number
        max_retries: Maximum number of retries allowed

    Returns:
        Formatted error message string
    """
    remaining = max_retries - retry_count
    retry_info = f"({remaining} attempt{'s' if remaining != 1 else ''} remaining)" if remaining > 0 else "(last attempt)"

    return f"\nError: {str(error)} {retry_info}\n"


def confirm_large_date_range(years: float) -> bool:
    """
    Ask user to confirm if they want to proceed with a large date range.

    Args:
        years: Number of years in the date range

    Returns:
        bool: True if user confirms, False otherwise
    """
    print(f"\nWarning: You've selected a {years:.1f} year date range.")
    print("This may result in:")
    print("  - Slower API response times")
    print("  - Large datasets")
    print("  - Potential API rate limit issues")

    while True:
        response = input("\nDo you want to continue? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'")
