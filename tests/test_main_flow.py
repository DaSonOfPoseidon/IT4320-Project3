# /usr/bin/env python3
# Integration tests for main application flow

from unittest.mock import patch, MagicMock
from datetime import datetime

import pandas as pd
import main


class TestEnvironmentValidation:
    """Test environment validation at startup."""

    @patch("main.EnvironmentValidator.validate_env_file")
    def test_successful_environment_validation(self, mock_validate):
        """Test successful environment validation."""
        mock_validate.return_value = True
        # Should not raise exception
        main.validate_environment()
        mock_validate.assert_called_once()

    @patch("main.EnvironmentValidator.validate_env_file")
    @patch("sys.exit")
    def test_failed_environment_validation(self, mock_exit, mock_validate):
        """Test failed environment validation exits gracefully."""
        from src.input_validator import ValidationError

        mock_validate.side_effect = ValidationError("API key not configured")
        main.validate_environment()
        mock_exit.assert_called_once_with(1)


class TestStockSymbolInput:
    """Test stock symbol input flow."""

    @patch("builtins.input", return_value="AAPL")
    def test_valid_symbol_first_attempt(self, mock_input):
        """Test valid symbol accepted on first attempt."""
        result = main.get_stock_symbol()
        assert result == "AAPL"
        mock_input.assert_called_once()

    @patch("builtins.input", side_effect=["", "MSFT"])
    @patch("builtins.print")
    def test_symbol_retry_after_empty(self, mock_print, mock_input):
        """Test retry after empty symbol."""
        result = main.get_stock_symbol()
        assert result == "MSFT"
        assert mock_input.call_count == 2

    @patch("builtins.input", side_effect=["AAA123", "GOOGL"])
    @patch("builtins.print")
    def test_symbol_retry_after_invalid(self, mock_print, mock_input):
        """Test retry after invalid symbol format."""
        result = main.get_stock_symbol()
        assert result == "GOOGL"
        assert mock_input.call_count == 2

    @patch("builtins.input", return_value="aapl")
    def test_symbol_uppercase_conversion(self, mock_input):
        """Test lowercase symbol converted to uppercase."""
        result = main.get_stock_symbol()
        assert result == "AAPL"

    @patch("builtins.input", side_effect=["", "", "", "VALID"])
    @patch("sys.exit")
    @patch("builtins.print")
    def test_symbol_max_retries_exceeded(self, mock_print, mock_exit, mock_input):
        """Test exit after exceeding max retries."""
        # Empty strings will fail validation
        main.get_stock_symbol()
        # Should exit after MAX_SYMBOL_INPUT_RETRIES
        mock_exit.assert_called_with(1)


class TestChartTypeInput:
    """Test chart type selection flow."""

    @patch("builtins.input", return_value="1")
    @patch("builtins.print")
    def test_valid_chart_type(self, mock_print, mock_input):
        """Test valid chart type selection."""
        result = main.get_chart_type()
        assert result == "line"

    @patch("builtins.input", return_value="2")
    @patch("builtins.print")
    def test_candlestick_selection(self, mock_print, mock_input):
        """Test candlestick chart selection."""
        result = main.get_chart_type()
        assert result == "candlestick"

    @patch("builtins.input", side_effect=["99", "3"])
    @patch("builtins.print")
    def test_chart_type_retry_after_invalid(self, mock_print, mock_input):
        """Test retry after invalid chart type."""
        result = main.get_chart_type()
        assert result == "ohlc"
        assert mock_input.call_count == 2


class TestTimeSeriesInput:
    """Test time series function selection flow."""

    @patch("builtins.input", return_value="1")
    @patch("builtins.print")
    def test_daily_time_series(self, mock_print, mock_input):
        """Test daily time series selection."""
        result, requires_interval = main.get_time_series_function()
        assert result == "TIME_SERIES_DAILY"
        assert requires_interval is False

    @patch("builtins.input", return_value="7")
    @patch("builtins.print")
    def test_intraday_time_series(self, mock_print, mock_input):
        """Test intraday time series selection requires interval."""
        result, requires_interval = main.get_time_series_function()
        assert result == "TIME_SERIES_INTRADAY"
        assert requires_interval is True


class TestIntradayIntervalInput:
    """Test intraday interval selection."""

    @patch("builtins.input", return_value="1")
    @patch("builtins.print")
    def test_1min_interval(self, mock_print, mock_input):
        """Test 1-minute interval selection."""
        result = main.get_intraday_interval()
        assert result == "1min"

    @patch("builtins.input", return_value="5")
    @patch("builtins.print")
    def test_60min_interval(self, mock_print, mock_input):
        """Test 60-minute interval selection."""
        result = main.get_intraday_interval()
        assert result == "60min"

    @patch("builtins.input", side_effect=["99", "3"])
    @patch("builtins.print")
    def test_interval_retry_after_invalid(self, mock_print, mock_input):
        """Test retry after invalid interval."""
        result = main.get_intraday_interval()
        assert result == "15min"
        assert mock_input.call_count == 2


class TestDateInput:
    """Test date input and validation."""

    @patch("builtins.input", return_value="2024-01-15")
    @patch("builtins.print")
    def test_valid_date_input(self, mock_print, mock_input):
        """Test valid date input."""
        date_str, date_obj = main.get_date_input("Enter date: ")
        assert date_str == "2024-01-15"
        assert date_obj.year == 2024
        assert date_obj.month == 1
        assert date_obj.day == 15

    @patch("builtins.input", side_effect=["invalid", "2024-01-15"])
    @patch("builtins.print")
    def test_date_retry_after_invalid_format(self, mock_print, mock_input):
        """Test retry after invalid date format."""
        date_str, date_obj = main.get_date_input("Enter date: ")
        assert date_str == "2024-01-15"
        assert mock_input.call_count == 2


class TestDateRangeInput:
    """Test date range input and validation."""

    @patch("builtins.input", side_effect=["2024-01-01", "2024-12-31"])
    @patch("builtins.print")
    def test_valid_date_range(self, mock_print, mock_input):
        """Test valid date range input."""
        begin, end = main.get_date_range()
        assert begin == "2024-01-01"
        assert end == "2024-12-31"

    @patch("builtins.input", side_effect=["2024-12-31", "2024-01-01", "2024-01-01", "2024-12-31"])
    @patch("builtins.print")
    def test_date_range_retry_when_end_before_begin(self, mock_print, mock_input):
        """Test retry when end date is before begin date."""
        begin, end = main.get_date_range()
        assert begin == "2024-01-01"
        assert end == "2024-12-31"
        # Should take 4 inputs: invalid begin, invalid end, valid begin, valid end
        assert mock_input.call_count == 4


class TestConfigurationSummary:
    """Test configuration summary display."""

    @patch("builtins.print")
    def test_summary_without_interval(self, mock_print):
        """Test summary display without interval."""
        main.display_configuration_summary(
            "AAPL", "line", "TIME_SERIES_DAILY", "2024-01-01", "2024-12-31"
        )
        # Verify print was called multiple times
        assert mock_print.call_count > 0

    @patch("builtins.print")
    def test_summary_with_interval(self, mock_print):
        """Test summary display with intraday interval."""
        main.display_configuration_summary(
            "MSFT", "candlestick", "TIME_SERIES_INTRADAY", "2024-01-01", "2024-01-31", "5min"
        )
        # Verify interval is included in output
        call_args_list = [str(call) for call in mock_print.call_args_list]
        has_interval = any("5min" in str(arg) for arg in call_args_list)
        assert has_interval


class TestMainFlow:
    """Integration tests for complete application flow."""

    @patch("main.validate_environment")
    @patch("main.get_stock_symbol", return_value="AAPL")
    @patch("main.get_chart_type", return_value="line")
    @patch("main.get_time_series_function", return_value=("TIME_SERIES_DAILY", False))
    @patch("main.get_date_range", return_value=("2024-01-01", "2024-12-31"))
    @patch("main.AlphaVantageClient")
    @patch("builtins.print")
    def test_complete_flow_without_interval(
        self, mock_print, mock_client, mock_date_range, mock_time_series, mock_chart, mock_symbol, mock_env
    ):
        """Test complete application flow without intraday interval."""
        # Mock the API client instance and its methods
        mock_instance = mock_client.return_value
        # Create a mock DataFrame with proper index
        mock_df = pd.DataFrame(
            {"close": [100, 101, 102]},
            index=pd.DatetimeIndex([datetime(2024, 1, 1), datetime(2024, 1, 2), datetime(2024, 1, 3)])
        )
        mock_instance.fetch_stock_data.return_value = mock_df

        main.main()
        # Verify all input functions were called
        mock_env.assert_called_once()
        mock_symbol.assert_called_once()
        mock_chart.assert_called_once()
        mock_time_series.assert_called_once()
        mock_date_range.assert_called_once()

    @patch("main.validate_environment")
    @patch("main.get_stock_symbol", return_value="MSFT")
    @patch("main.get_chart_type", return_value="candlestick")
    @patch("main.get_time_series_function", return_value=("TIME_SERIES_INTRADAY", True))
    @patch("main.get_intraday_interval", return_value="5min")
    @patch("main.get_date_range", return_value=("2024-01-01", "2024-01-31"))
    @patch("main.AlphaVantageClient")
    @patch("builtins.print")
    def test_complete_flow_with_interval(
        self,
        mock_print,
        mock_client,
        mock_date_range,
        mock_interval,
        mock_time_series,
        mock_chart,
        mock_symbol,
        mock_env,
    ):
        """Test complete application flow with intraday interval."""
        # Mock the API client instance and its methods
        mock_instance = mock_client.return_value
        # Create a mock DataFrame with proper index
        mock_df = pd.DataFrame(
            {"close": [100, 101, 102]},
            index=pd.DatetimeIndex([datetime(2024, 1, 1), datetime(2024, 1, 2), datetime(2024, 1, 3)])
        )
        mock_instance.fetch_stock_data.return_value = mock_df

        main.main()
        # Verify interval function was called for intraday
        mock_interval.assert_called_once()

    @patch("main.validate_environment")
    @patch("main.get_stock_symbol", side_effect=KeyboardInterrupt)
    @patch("sys.exit")
    @patch("builtins.print")
    def test_keyboard_interrupt_handling(self, mock_print, mock_exit, mock_symbol, mock_env):
        """Test graceful handling of keyboard interrupt."""
        main.main()
        mock_exit.assert_called_with(0)

    @patch("main.validate_environment")
    @patch("main.get_stock_symbol", side_effect=Exception("Unexpected error"))
    @patch("sys.exit")
    @patch("builtins.print")
    def test_unexpected_error_handling(self, mock_print, mock_exit, mock_symbol, mock_env):
        """Test handling of unexpected errors."""
        main.main()
        mock_exit.assert_called_with(1)
