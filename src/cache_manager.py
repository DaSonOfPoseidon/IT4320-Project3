# /usr/bin/env python3
# Cache Manager for Stock Data API Responses
# Implements disk-based caching to minimize API calls and support offline usage

import os
import pickle
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from typing import Optional, Dict, Any


# Cache configuration
CACHE_DIR = ".cache/stock_data"
CACHE_EXPIRATION_HOURS = 24


class CacheManager:
    """
    Manages disk-based caching of API responses to minimize API calls.

    Features:
    - Stores pandas DataFrames as pickle files
    - Automatic cache expiration (24 hours default)
    - Cache key generation based on query parameters
    - Cache validation and cleanup
    """

    def __init__(self, cache_dir: str = CACHE_DIR, expiration_hours: int = CACHE_EXPIRATION_HOURS):
        """
        Initialize cache manager.

        Args:
            cache_dir: Directory path for cache storage
            expiration_hours: Hours before cached data expires
        """
        self.cache_dir = Path(cache_dir)
        self.expiration_hours = expiration_hours

        # Create cache directory if it doesn't exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _generate_cache_key(
        self, symbol: str, function: str, interval: Optional[str] = None, outputsize: str = "full"
    ) -> str:
        """
        Generate unique cache key based on query parameters.

        Args:
            symbol: Stock ticker symbol
            function: Alpha Vantage time series function
            interval: Intraday interval (for TIME_SERIES_INTRADAY)
            outputsize: API output size parameter

        Returns:
            Cache key string
        """
        if interval:
            return f"{symbol}_{function}_{interval}_{outputsize}.pkl"
        return f"{symbol}_{function}_{outputsize}.pkl"

    def _get_cache_path(self, cache_key: str) -> Path:
        """
        Get full file path for cache key.

        Args:
            cache_key: Cache key string

        Returns:
            Path object for cache file
        """
        return self.cache_dir / cache_key

    def is_cache_valid(self, cache_key: str) -> bool:
        """
        Check if cached data exists and is not expired.

        Args:
            cache_key: Cache key to validate

        Returns:
            True if cache exists and is valid, False otherwise
        """
        cache_path = self._get_cache_path(cache_key)

        if not cache_path.exists():
            return False

        # Check file modification time
        mod_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
        expiration_time = datetime.now() - timedelta(hours=self.expiration_hours)

        return mod_time > expiration_time

    def get_cached_data(
        self, symbol: str, function: str, interval: Optional[str] = None, outputsize: str = "full"
    ) -> Optional[pd.DataFrame]:
        """
        Retrieve cached data if available and valid.

        Args:
            symbol: Stock ticker symbol
            function: Alpha Vantage time series function
            interval: Intraday interval (for TIME_SERIES_INTRADAY)
            outputsize: API output size parameter

        Returns:
            DataFrame if cache valid, None otherwise
        """
        cache_key = self._generate_cache_key(symbol, function, interval, outputsize)

        if not self.is_cache_valid(cache_key):
            return None

        cache_path = self._get_cache_path(cache_key)

        try:
            with open(cache_path, "rb") as f:
                data = pickle.load(f)
            return data
        except Exception as e:
            print(f"Warning: Failed to load cache file {cache_key}: {e}")
            return None

    def save_to_cache(
        self,
        data: pd.DataFrame,
        symbol: str,
        function: str,
        interval: Optional[str] = None,
        outputsize: str = "full",
    ) -> bool:
        """
        Save DataFrame to cache.

        Args:
            data: pandas DataFrame to cache
            symbol: Stock ticker symbol
            function: Alpha Vantage time series function
            interval: Intraday interval (for TIME_SERIES_INTRADAY)
            outputsize: API output size parameter

        Returns:
            True if successfully saved, False otherwise
        """
        cache_key = self._generate_cache_key(symbol, function, interval, outputsize)
        cache_path = self._get_cache_path(cache_key)

        try:
            with open(cache_path, "wb") as f:
                pickle.dump(data, f)
            return True
        except Exception as e:
            print(f"Warning: Failed to save cache file {cache_key}: {e}")
            return False

    def clear_expired_cache(self) -> int:
        """
        Remove all expired cache files.

        Returns:
            Number of files removed
        """
        removed_count = 0

        for cache_file in self.cache_dir.glob("*.pkl"):
            mod_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            expiration_time = datetime.now() - timedelta(hours=self.expiration_hours)

            if mod_time <= expiration_time:
                try:
                    cache_file.unlink()
                    removed_count += 1
                except Exception as e:
                    print(f"Warning: Failed to remove expired cache {cache_file.name}: {e}")

        return removed_count

    def clear_all_cache(self) -> int:
        """
        Remove all cache files.

        Returns:
            Number of files removed
        """
        removed_count = 0

        for cache_file in self.cache_dir.glob("*.pkl"):
            try:
                cache_file.unlink()
                removed_count += 1
            except Exception as e:
                print(f"Warning: Failed to remove cache {cache_file.name}: {e}")

        return removed_count

    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get information about current cache state.

        Returns:
            Dictionary with cache statistics
        """
        cache_files = list(self.cache_dir.glob("*.pkl"))
        total_files = len(cache_files)

        valid_files = 0
        expired_files = 0
        total_size = 0

        for cache_file in cache_files:
            total_size += cache_file.stat().st_size

            mod_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            expiration_time = datetime.now() - timedelta(hours=self.expiration_hours)

            if mod_time > expiration_time:
                valid_files += 1
            else:
                expired_files += 1

        return {
            "total_files": total_files,
            "valid_files": valid_files,
            "expired_files": expired_files,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "cache_directory": str(self.cache_dir),
        }
