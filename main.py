# /usr/bin/env python3
# Stock Data Visualization CLI Application
# Alpha Vantage API Integration for Historical Stock Data Analysis

import sys
from src.constants import (
    CHART_TYPES,
    TIME_SERIES_FUNCTIONS,
    INTRADAY_INTERVALS,
    MAX_SYMBOL_INPUT_RETRIES,
    MAX_CHOICE_INPUT_RETRIES,
    MAX_DATE_INPUT_RETRIES,
)
from src.input_validator import (
    ValidationError,
    EnvironmentValidator,
    StockSymbolValidator,
    DateValidator,
    ChoiceValidator,
    format_error_message,
)


def validate_environment():
    """
    Validate environment configuration at startup.

    Raises:
        SystemExit: If environment validation fails
    """
    try:
        EnvironmentValidator.validate_env_file()
        print("Environment configuration validated successfully\n")
    except ValidationError as e:
        print(f"\n{e}\n")
        sys.exit(1)


from datetime import datetime
from src.api_client import (
    AlphaVantageClient,
    APIError,
    RateLimitError,
    InvalidSymbolError,
    NetworkError,
)


def get_stock_symbol():
    """
    Get and validate stock symbol from user input with retry logic.

    Returns:
        str: Validated stock symbol in uppercase

    Raises:
        SystemExit: If maximum retries exceeded
    """
    retry_count = 0

    while retry_count < MAX_SYMBOL_INPUT_RETRIES:
        try:
            symbol = input("Enter the stock symbol (e.g., AAPL, MSFT): ").strip()
            return StockSymbolValidator.validate(symbol)
        except ValidationError as e:
            retry_count += 1
            if retry_count >= MAX_SYMBOL_INPUT_RETRIES:
                print(f"\nMaximum retry attempts exceeded. Exiting.")
                sys.exit(1)
            print(format_error_message(e, retry_count, MAX_SYMBOL_INPUT_RETRIES))
        except KeyboardInterrupt:
            print("\n\nInput interrupted by user. Exiting.")
            sys.exit(0)


def get_chart_type():
    """
    Get chart type preference from user with validation.

    Returns:
        str: Chart type key (e.g., 'line', 'candlestick')
    """
    print("\nAvailable chart types:")
    for choice, config in CHART_TYPES.items():
        print(f"{choice}. {config['display']}")

    retry_count = 0
    while retry_count < MAX_CHOICE_INPUT_RETRIES:
        try:
            choice = input(f"\nSelect chart type (1-{len(CHART_TYPES)}): ").strip()
            validated = ChoiceValidator.validate_choice(choice, CHART_TYPES, "Chart type")
            return CHART_TYPES[validated]["key"]
        except ValidationError as e:
            retry_count += 1
            if retry_count >= MAX_CHOICE_INPUT_RETRIES:
                print(f"\nMaximum retry attempts exceeded. Exiting.")
                sys.exit(1)
            print(format_error_message(e, retry_count, MAX_CHOICE_INPUT_RETRIES))
        except KeyboardInterrupt:
            print("\n\nInput interrupted by user. Exiting.")
            sys.exit(0)


def get_time_series_function():
    """
    Get time series function from user with validation.

    Returns:
        tuple: (time_series_key, requires_interval_bool)
    """
    print("\nAvailable time series functions:")
    for choice, config in TIME_SERIES_FUNCTIONS.items():
        print(f"{choice}. {config['display']}")

    retry_count = 0
    while retry_count < MAX_CHOICE_INPUT_RETRIES:
        try:
            choice = input(
                f"\nSelect time series function (1-{len(TIME_SERIES_FUNCTIONS)}): "
            ).strip()
            validated = ChoiceValidator.validate_choice(
                choice, TIME_SERIES_FUNCTIONS, "Time series function"
            )
            config = TIME_SERIES_FUNCTIONS[validated]
            return config["key"], config["requires_interval"]
        except ValidationError as e:
            retry_count += 1
            if retry_count >= MAX_CHOICE_INPUT_RETRIES:
                print(f"\nMaximum retry attempts exceeded. Exiting.")
                sys.exit(1)
            print(format_error_message(e, retry_count, MAX_CHOICE_INPUT_RETRIES))
        except KeyboardInterrupt:
            print("\n\nInput interrupted by user. Exiting.")
            sys.exit(0)


def get_intraday_interval():
    """
    Get intraday interval selection for TIME_SERIES_INTRADAY.

    Returns:
        str: Interval key (e.g., '1min', '5min', '15min')
    """
    print("\nIntraday intervals:")
    for choice, config in INTRADAY_INTERVALS.items():
        print(f"{choice}. {config['display']} - {config['description']}")

    retry_count = 0
    while retry_count < MAX_CHOICE_INPUT_RETRIES:
        try:
            choice = input(f"\nSelect interval (1-{len(INTRADAY_INTERVALS)}): ").strip()
            validated = ChoiceValidator.validate_choice(choice, INTRADAY_INTERVALS, "Interval")
            return INTRADAY_INTERVALS[validated]["key"]
        except ValidationError as e:
            retry_count += 1
            if retry_count >= MAX_CHOICE_INPUT_RETRIES:
                print(f"\nMaximum retry attempts exceeded. Exiting.")
                sys.exit(1)
            print(format_error_message(e, retry_count, MAX_CHOICE_INPUT_RETRIES))
        except KeyboardInterrupt:
            print("\n\nInput interrupted by user. Exiting.")
            sys.exit(0)


def get_intraday_interval():
    # Get intraday interval selection
    print("\nAvailable intraday intervals:")
    print("1. 1 minute")
    print("2. 5 minutes")
    print("3. 15 minutes")
    print("4. 30 minutes")
    print("5. 60 minutes")

    while True:
        choice = input("\nSelect interval (1-5): ").strip()
        intervals = {"1": "1min", "2": "5min", "3": "15min", "4": "30min", "5": "60min"}
        if choice in intervals:
            return intervals[choice]
        print("Error: Please enter a number between 1 and 5")


def get_date_input(prompt):
    """
    Get and validate a single date input with enhanced validation.

    Args:
        prompt: Input prompt to display to user

    Returns:
        tuple: (date_string, datetime_object)
    """
    retry_count = 0

    while retry_count < MAX_DATE_INPUT_RETRIES:
        try:
            date_str = input(prompt).strip()
            date_str, date_obj = DateValidator.parse_date(date_str)

            # Check for weekend warning
            weekend_warning = DateValidator.check_weekend(date_obj)
            if weekend_warning:
                print(f"  {weekend_warning}")

            return date_str, date_obj
        except ValidationError as e:
            retry_count += 1
            if retry_count >= MAX_DATE_INPUT_RETRIES:
                print(f"\nMaximum retry attempts exceeded. Exiting.")
                sys.exit(1)
            print(format_error_message(e, retry_count, MAX_DATE_INPUT_RETRIES))
        except KeyboardInterrupt:
            print("\n\nInput interrupted by user. Exiting.")
            sys.exit(0)


def get_date_range():
    """
    Get and validate complete date range with enhanced checks.

    Returns:
        tuple: (begin_date_string, end_date_string)
    """
    retry_count = 0

    while retry_count < MAX_DATE_INPUT_RETRIES:
        try:
            # Get begin date
            begin_date_str, begin_date = get_date_input("Enter begin date (YYYY-MM-DD): ")

            # Get end date
            end_date_str, end_date = get_date_input("Enter end date (YYYY-MM-DD): ")

            # Validate range
            result = DateValidator.validate_date_range(
                begin_date, end_date, begin_date_str, end_date_str
            )

            # Handle warning message if present
            if len(result) == 3 and result[2]:
                print(f"\n  {result[2]}")

            return result[0], result[1]

        except ValidationError as e:
            retry_count += 1
            if retry_count >= MAX_DATE_INPUT_RETRIES:
                print(f"\nMaximum retry attempts exceeded. Exiting.")
                sys.exit(1)
            print(format_error_message(e, retry_count, MAX_DATE_INPUT_RETRIES))
        except KeyboardInterrupt:
            print("\n\nInput interrupted by user. Exiting.")
            sys.exit(0)


def display_configuration_summary(
    symbol, chart_type, time_series, begin_date, end_date, interval=None
):
    """
    Display collected configuration in a formatted summary.

    Args:
        symbol: Stock symbol
        chart_type: Selected chart type
        time_series: Selected time series function
        begin_date: Start date string
        end_date: End date string
        interval: Optional intraday interval
    """
    print(f"\n{'=' * 50}")
    print("Configuration Summary")
    print(f"{'=' * 50}")
    print(f"Stock Symbol:    {symbol}")
    print(f"Chart Type:      {chart_type}")
    print(f"Time Series:     {time_series}")
    if interval:
        print(f"Interval:        {interval}")
    print(f"Date Range:      {begin_date} to {end_date}")
    print(f"{'=' * 50}\n")


def main():
    """Main application entry point with comprehensive error handling."""
    print("=" * 50)
    print("Stock Data Visualization Tool")
    print("Alpha Vantage API Integration")
    print("=" * 50)
    print()

    try:
        # Validate environment configuration
        validate_environment()

        # Collect user inputs with validation
        symbol = get_stock_symbol()
        chart_type = get_chart_type()
        time_series, requires_interval = get_time_series_function()

        # Get interval if intraday time series selected
        interval = None
        if requires_interval:
            interval = get_intraday_interval()

        begin_date, end_date = get_date_range()

        # Display configuration summary
        display_configuration_summary(
            symbol, chart_type, time_series, begin_date, end_date, interval
        )

        # Placeholder for future functionality (Phases 2-5)
        print(f"[PLACEHOLDER] Fetching {time_series} data for {symbol}...")
        if interval:
            print(f"[PLACEHOLDER] Using {interval} interval...")
        print(f"[PLACEHOLDER] Filtering data from {begin_date} to {end_date}...")
        # Display collected information
        print(f"\n=== Configuration Summary ===")
        print(f"Stock Symbol: {symbol}")
        print(f"Chart Type: {chart_type}")
        print(f"Time Series: {time_series}")
        if interval:
            print(f"Interval: {interval}")
        print(f"Date Range: {begin_date} to {end_date}")
        print("=" * 30)

        # Initialize API client
        print()
        try:
            client = AlphaVantageClient()
        except APIError as e:
            print(f"\nError initializing API client: {e}")
            print("Please ensure your .env file is configured with a valid API key.")
            sys.exit(1)

        # Fetch stock data from API
        try:
            stock_data = client.fetch_stock_data(symbol, time_series, interval)
            print(f"\nSuccessfully retrieved {len(stock_data)} data points")
            print(
                f"Date range in data: {stock_data.index[0].date()} to {stock_data.index[-1].date()}"
            )

            # Display preview of data
            print(f"\nData preview (first 5 rows):")
            print(stock_data.head())

        except RateLimitError as e:
            print(f"\n{e}")
            print("Please try again tomorrow or use a different API key.")
            sys.exit(1)
        except InvalidSymbolError as e:
            print(f"\n{e}")
            print("Please verify the stock symbol and try again.")
            sys.exit(1)
        except NetworkError as e:
            print(f"\n{e}")
            print("Please check your internet connection and try again.")
            sys.exit(1)
        except APIError as e:
            print(f"\nAPI Error: {e}")
            sys.exit(1)

        # Placeholder for future functionality (Phase 4 and 5)
        print(f"\n[PLACEHOLDER] Filtering data from {begin_date} to {end_date}...")
        print(f"[PLACEHOLDER] Generating {chart_type} chart...")
        print("[PLACEHOLDER] Opening chart in default browser...")

        print("\nApplication completed successfully!")

    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Please report this issue if it persists.")
        sys.exit(1)


if __name__ == "__main__":
    main()
