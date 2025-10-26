# /usr/bin/env python3
# Basic tests for API client and cache manager

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime, timedelta
from src.api_client import (
    AlphaVantageClient, APIError, RateLimitError,
    InvalidSymbolError, NetworkError
)
from src.cache_manager import CacheManager


class TestAPIClient:
    """Basic tests for Alpha Vantage API client."""

    @patch('src.api_client.os.getenv')
    def test_client_initialization_success(self, mock_getenv):
        """Test successful client initialization with API key."""
        mock_getenv.return_value = 'test_api_key_123'
        client = AlphaVantageClient()
        assert client.api_key == 'test_api_key_123'
        assert client.use_cache is True

    @patch('src.api_client.os.getenv')
    def test_client_initialization_no_api_key(self, mock_getenv):
        """Test client initialization fails without API key."""
        mock_getenv.return_value = None
        with pytest.raises(APIError, match="not configured"):
            AlphaVantageClient()

    @patch('src.api_client.os.getenv')
    def test_client_initialization_placeholder_key(self, mock_getenv):
        """Test client initialization fails with placeholder key."""
        mock_getenv.return_value = 'your_api_key_here'
        with pytest.raises(APIError, match="not configured"):
            AlphaVantageClient()

    @patch('src.api_client.os.getenv')
    @patch('src.api_client.requests.get')
    def test_successful_api_request(self, mock_get, mock_getenv):
        """Test successful API request and DataFrame parsing."""
        mock_getenv.return_value = 'test_api_key'

        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'Time Series (Daily)': {
                '2024-01-03': {
                    '1. open': '100.0',
                    '2. high': '105.0',
                    '3. low': '99.0',
                    '4. close': '103.0',
                    '5. volume': '1000000'
                },
                '2024-01-02': {
                    '1. open': '98.0',
                    '2. high': '101.0',
                    '3. low': '97.0',
                    '4. close': '100.0',
                    '5. volume': '950000'
                }
            }
        }
        mock_get.return_value = mock_response

        client = AlphaVantageClient(use_cache=False)
        df = client.fetch_stock_data('AAPL', 'TIME_SERIES_DAILY')

        # Verify DataFrame structure
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert 'Open' in df.columns
        assert 'High' in df.columns
        assert 'Low' in df.columns
        assert 'Close' in df.columns
        assert 'Volume' in df.columns

    @patch('src.api_client.os.getenv')
    @patch('src.api_client.requests.get')
    def test_rate_limit_error(self, mock_get, mock_getenv):
        """Test rate limit detection."""
        mock_getenv.return_value = 'test_api_key'

        mock_response = MagicMock()
        mock_response.json.return_value = {
            'Note': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day.'
        }
        mock_get.return_value = mock_response

        client = AlphaVantageClient(use_cache=False)

        with pytest.raises(RateLimitError, match="rate limit"):
            client.fetch_stock_data('AAPL', 'TIME_SERIES_DAILY')

    @patch('src.api_client.os.getenv')
    @patch('src.api_client.requests.get')
    def test_invalid_symbol_error(self, mock_get, mock_getenv):
        """Test invalid symbol detection."""
        mock_getenv.return_value = 'test_api_key'

        mock_response = MagicMock()
        mock_response.json.return_value = {
            'Error Message': 'Invalid API call. Please retry or visit the documentation'
        }
        mock_get.return_value = mock_response

        client = AlphaVantageClient(use_cache=False)

        with pytest.raises(InvalidSymbolError, match="Invalid symbol"):
            client.fetch_stock_data('INVALID', 'TIME_SERIES_DAILY')

    @patch('src.api_client.os.getenv')
    @patch('src.api_client.requests.get')
    @patch('src.api_client.time.sleep')  # Mock sleep to speed up test
    def test_network_error_retry(self, mock_sleep, mock_get, mock_getenv):
        """Test network error retry logic."""
        mock_getenv.return_value = 'test_api_key'

        # Simulate connection errors
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        client = AlphaVantageClient(use_cache=False)

        with pytest.raises(NetworkError, match="after multiple retries"):
            client.fetch_stock_data('AAPL', 'TIME_SERIES_DAILY')

        # Verify retry attempts (initial + 3 retries = 4 total calls)
        assert mock_get.call_count == 4  # 1 initial + MAX_API_RETRIES


class TestCacheManager:
    """Basic tests for cache manager."""

    def test_cache_key_generation(self, tmp_path):
        """Test cache key generation."""
        cache = CacheManager(cache_dir=str(tmp_path), expiration_hours=24)

        # Without interval
        key1 = cache._generate_cache_key('AAPL', 'TIME_SERIES_DAILY')
        assert key1 == 'AAPL_TIME_SERIES_DAILY_full.pkl'

        # With interval
        key2 = cache._generate_cache_key('MSFT', 'TIME_SERIES_INTRADAY', '5min')
        assert key2 == 'MSFT_TIME_SERIES_INTRADAY_5min_full.pkl'

    def test_cache_save_and_retrieve(self, tmp_path):
        """Test saving and retrieving cached data."""
        cache = CacheManager(cache_dir=str(tmp_path), expiration_hours=24)

        # Create test DataFrame
        test_data = pd.DataFrame({
            'Open': [100, 101],
            'Close': [102, 103]
        })

        # Save to cache
        success = cache.save_to_cache(test_data, 'AAPL', 'TIME_SERIES_DAILY')
        assert success is True

        # Retrieve from cache
        retrieved = cache.get_cached_data('AAPL', 'TIME_SERIES_DAILY')
        assert retrieved is not None
        pd.testing.assert_frame_equal(retrieved, test_data)

    def test_cache_expiration(self, tmp_path):
        """Test cache expiration logic."""
        # Create cache with 0 hour expiration (immediately expired)
        cache = CacheManager(cache_dir=str(tmp_path), expiration_hours=0)

        test_data = pd.DataFrame({'A': [1, 2, 3]})
        cache.save_to_cache(test_data, 'TEST', 'TIME_SERIES_DAILY')

        # Wait a moment to ensure file is older than expiration
        import time
        time.sleep(0.1)

        # Should return None for expired cache
        retrieved = cache.get_cached_data('TEST', 'TIME_SERIES_DAILY')
        assert retrieved is None
