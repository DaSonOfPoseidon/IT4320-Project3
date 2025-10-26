# /usr/bin/env python3
# Unit tests for input validation module

import pytest
import os
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from src.input_validator import (
    ValidationError,
    StockSymbolValidator,
    DateValidator,
    ChoiceValidator,
    EnvironmentValidator,
    format_error_message,
)
from src.constants import CHART_TYPES, TIME_SERIES_FUNCTIONS


class TestStockSymbolValidator:
    """Test cases for stock symbol validation."""

    def test_valid_single_letter_symbol(self):
        """Test single letter symbol (e.g., F for Ford)."""
        assert StockSymbolValidator.validate("F") == "F"
        assert StockSymbolValidator.validate("f") == "F"

    def test_valid_multi_letter_symbols(self):
        """Test common multi-letter symbols."""
        assert StockSymbolValidator.validate("AAPL") == "AAPL"
        assert StockSymbolValidator.validate("MSFT") == "MSFT"
        assert StockSymbolValidator.validate("GOOGL") == "GOOGL"
        assert StockSymbolValidator.validate("aapl") == "AAPL"

    def test_whitespace_trimming(self):
        """Test that whitespace is properly trimmed."""
        assert StockSymbolValidator.validate("  AAPL  ") == "AAPL"
        assert StockSymbolValidator.validate("\tMSFT\n") == "MSFT"

    def test_empty_symbol(self):
        """Test empty symbol validation."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            StockSymbolValidator.validate("")
        with pytest.raises(ValidationError, match="cannot be empty"):
            StockSymbolValidator.validate("   ")

    def test_symbol_too_long(self):
        """Test symbol exceeding maximum length."""
        with pytest.raises(ValidationError, match="too long"):
            StockSymbolValidator.validate("ABCDEF")  # 6 characters, max is 5

    def test_symbol_with_numbers(self):
        """Test symbols containing numbers (invalid)."""
        with pytest.raises(ValidationError, match="only letters"):
            StockSymbolValidator.validate("AAPL1")
        with pytest.raises(ValidationError, match="only letters"):
            StockSymbolValidator.validate("123")

    def test_symbol_with_special_characters(self):
        """Test symbols with special characters (invalid)."""
        with pytest.raises(ValidationError, match="only letters"):
            StockSymbolValidator.validate("AAPL-")
        with pytest.raises(ValidationError, match="only letters"):
            StockSymbolValidator.validate("AA.PL")
        with pytest.raises(ValidationError, match="only letters"):
            StockSymbolValidator.validate("AAPL!")


class TestDateValidator:
    """Test cases for date validation."""

    def test_valid_date_parsing(self):
        """Test parsing of valid dates."""
        date_str, date_obj = DateValidator.parse_date("2024-01-15")
        assert date_str == "2024-01-15"
        assert isinstance(date_obj, datetime)
        assert date_obj.year == 2024
        assert date_obj.month == 1
        assert date_obj.day == 15

    def test_invalid_date_format(self):
        """Test invalid date format handling."""
        with pytest.raises(ValidationError, match="Invalid date"):
            DateValidator.parse_date("01/15/2024")
        with pytest.raises(ValidationError, match="Invalid date"):
            DateValidator.parse_date("15-01-2024")
        with pytest.raises(ValidationError, match="Invalid date"):
            DateValidator.parse_date("not-a-date")

    def test_future_date_rejection(self):
        """Test that future dates are rejected."""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        with pytest.raises(ValidationError, match="cannot be in the future"):
            DateValidator.parse_date(tomorrow)

    def test_today_date_accepted(self):
        """Test that today's date is accepted."""
        today = datetime.now().strftime("%Y-%m-%d")
        date_str, date_obj = DateValidator.parse_date(today)
        assert date_str == today

    def test_past_date_accepted(self):
        """Test that past dates are accepted."""
        past = "2020-01-01"
        date_str, date_obj = DateValidator.parse_date(past)
        assert date_str == past

    def test_invalid_calendar_dates(self):
        """Test invalid calendar dates."""
        with pytest.raises(ValidationError):
            DateValidator.parse_date("2024-02-30")  # Feb doesn't have 30 days
        with pytest.raises(ValidationError):
            DateValidator.parse_date("2024-13-01")  # Invalid month

    def test_leap_year_handling(self):
        """Test leap year date handling."""
        # 2024 is a leap year
        date_str, date_obj = DateValidator.parse_date("2024-02-29")
        assert date_str == "2024-02-29"

        # 2023 is not a leap year
        with pytest.raises(ValidationError):
            DateValidator.parse_date("2023-02-29")

    def test_date_range_validation_valid(self):
        """Test valid date range validation."""
        begin = datetime(2024, 1, 1)
        end = datetime(2024, 12, 31)
        result = DateValidator.validate_date_range(begin, end, "2024-01-01", "2024-12-31")
        assert result[0] == "2024-01-01"
        assert result[1] == "2024-12-31"

    def test_date_range_validation_same_date(self):
        """Test date range with same begin and end date."""
        date = datetime(2024, 1, 1)
        result = DateValidator.validate_date_range(date, date, "2024-01-01", "2024-01-01")
        assert result[0] == "2024-01-01"

    def test_date_range_validation_end_before_begin(self):
        """Test date range where end is before begin."""
        begin = datetime(2024, 12, 31)
        end = datetime(2024, 1, 1)
        with pytest.raises(ValidationError, match="on or after"):
            DateValidator.validate_date_range(begin, end, "2024-12-31", "2024-01-01")

    def test_date_range_too_large(self):
        """Test date range exceeding maximum years."""
        begin = datetime(2000, 1, 1)
        end = datetime(2025, 1, 1)  # 25 years > MAX_DATE_RANGE_YEARS (20)
        with pytest.raises(ValidationError, match="too large"):
            DateValidator.validate_date_range(begin, end, "2000-01-01", "2025-01-01")

    def test_weekend_detection_saturday(self):
        """Test weekend detection for Saturday."""
        saturday = datetime(2024, 1, 6)  # January 6, 2024 is Saturday
        warning = DateValidator.check_weekend(saturday)
        assert warning is not None
        assert "Saturday" in warning

    def test_weekend_detection_sunday(self):
        """Test weekend detection for Sunday."""
        sunday = datetime(2024, 1, 7)  # January 7, 2024 is Sunday
        warning = DateValidator.check_weekend(sunday)
        assert warning is not None
        assert "Sunday" in warning

    def test_weekday_no_warning(self):
        """Test that weekdays don't generate warnings."""
        monday = datetime(2024, 1, 8)  # January 8, 2024 is Monday
        warning = DateValidator.check_weekend(monday)
        assert warning is None


class TestChoiceValidator:
    """Test cases for menu choice validation."""

    def test_valid_chart_type_choice(self):
        """Test valid chart type selection."""
        result = ChoiceValidator.validate_choice("1", CHART_TYPES, "Chart type")
        assert result == "1"

    def test_valid_time_series_choice(self):
        """Test valid time series selection."""
        result = ChoiceValidator.validate_choice("3", TIME_SERIES_FUNCTIONS, "Time series")
        assert result == "3"

    def test_empty_choice(self):
        """Test empty choice handling."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            ChoiceValidator.validate_choice("", CHART_TYPES, "Chart type")

    def test_invalid_choice_number(self):
        """Test invalid choice number."""
        with pytest.raises(ValidationError, match="Invalid"):
            ChoiceValidator.validate_choice("99", CHART_TYPES, "Chart type")

    def test_non_numeric_choice(self):
        """Test non-numeric choice."""
        with pytest.raises(ValidationError, match="Invalid"):
            ChoiceValidator.validate_choice("abc", CHART_TYPES, "Chart type")

    def test_whitespace_handling(self):
        """Test that whitespace is properly trimmed in choices."""
        result = ChoiceValidator.validate_choice("  1  ", CHART_TYPES, "Chart type")
        assert result == "1"


class TestEnvironmentValidator:
    """Test cases for environment validation."""

    @patch("os.path.exists")
    def test_missing_env_file(self, mock_exists):
        """Test validation when .env file is missing."""
        mock_exists.return_value = False
        with pytest.raises(ValidationError, match="not found"):
            EnvironmentValidator.validate_env_file()

    @patch("os.path.exists")
    @patch("src.input_validator.load_dotenv")
    @patch("os.getenv")
    def test_empty_api_key(self, mock_getenv, mock_load_dotenv, mock_exists):
        """Test validation when API key is empty."""
        mock_exists.return_value = True
        mock_getenv.return_value = ""
        with pytest.raises(ValidationError, match="not configured"):
            EnvironmentValidator.validate_env_file()

    @patch("os.path.exists")
    @patch("src.input_validator.load_dotenv")
    @patch("os.getenv")
    def test_placeholder_api_key(self, mock_getenv, mock_load_dotenv, mock_exists):
        """Test validation when API key is placeholder."""
        mock_exists.return_value = True
        mock_getenv.return_value = "your_api_key_here"
        with pytest.raises(ValidationError, match="not configured"):
            EnvironmentValidator.validate_env_file()

    @patch("os.path.exists")
    @patch("src.input_validator.load_dotenv")
    @patch("os.getenv")
    def test_valid_api_key(self, mock_getenv, mock_load_dotenv, mock_exists):
        """Test validation with valid API key."""
        mock_exists.return_value = True
        mock_getenv.return_value = "VALID_API_KEY_123"
        assert EnvironmentValidator.validate_env_file() is True


class TestErrorFormatting:
    """Test cases for error message formatting."""

    def test_format_error_with_retries_remaining(self):
        """Test error formatting with retries remaining."""
        error = ValidationError("Test error")
        message = format_error_message(error, 1, 3)
        assert "Test error" in message
        assert "2 attempts remaining" in message

    def test_format_error_last_attempt(self):
        """Test error formatting on last attempt."""
        error = ValidationError("Test error")
        message = format_error_message(error, 3, 3)
        assert "Test error" in message
        assert "last attempt" in message

    def test_format_error_single_attempt_remaining(self):
        """Test singular 'attempt' vs plural 'attempts'."""
        error = ValidationError("Test error")
        message = format_error_message(error, 2, 3)
        assert "1 attempt remaining" in message
        assert "attempts" not in message or "1 attempt" in message
