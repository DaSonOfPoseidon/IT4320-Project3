# /usr/bin/env python3
# Stock Data Visualization CLI Application
# Alpha Vantage API Integration for Historical Stock Data Analysis

import sys
from datetime import datetime

def get_stock_symbol():
    # Get stock symbol from user input
    symbol = input("Enter the stock symbol (e.g., AAPL, MSFT): ").strip().upper()
    if not symbol:
        print("Error: Stock symbol cannot be empty")
        return get_stock_symbol()
    return symbol

def get_chart_type():
    # Get chart type preference from user
    print("\nAvailable chart types:")
    print("1. Line Chart (Close Price)")
    print("2. Candlestick Chart")
    print("3. OHLC Bar Chart")
    print("4. Volume Overlay Chart")

    while True:
        choice = input("\nSelect chart type (1-4): ").strip()
        chart_types = {
            '1': 'line',
            '2': 'candlestick',
            '3': 'ohlc',
            '4': 'volume'
        }
        if choice in chart_types:
            return chart_types[choice]
        print("Error: Please enter a number between 1 and 4")

def get_time_series_function():
    # Get time series function from user
    print("\nAvailable time series functions:")
    print("1. Daily (TIME_SERIES_DAILY)")
    print("2. Daily Adjusted (TIME_SERIES_DAILY_ADJUSTED)")
    print("3. Weekly (TIME_SERIES_WEEKLY)")
    print("4. Weekly Adjusted (TIME_SERIES_WEEKLY_ADJUSTED)")
    print("5. Monthly (TIME_SERIES_MONTHLY)")
    print("6. Monthly Adjusted (TIME_SERIES_MONTHLY_ADJUSTED)")
    print("7. Intraday (TIME_SERIES_INTRADAY)")

    while True:
        choice = input("\nSelect time series function (1-7): ").strip()
        functions = {
            '1': 'TIME_SERIES_DAILY',
            '2': 'TIME_SERIES_DAILY_ADJUSTED',
            '3': 'TIME_SERIES_WEEKLY',
            '4': 'TIME_SERIES_WEEKLY_ADJUSTED',
            '5': 'TIME_SERIES_MONTHLY',
            '6': 'TIME_SERIES_MONTHLY_ADJUSTED',
            '7': 'TIME_SERIES_INTRADAY'
        }
        if choice in functions:
            return functions[choice]
        print("Error: Please enter a number between 1 and 7")

def get_date_input(prompt):
    # Get and validate date input in YYYY-MM-DD format
    while True:
        date_str = input(prompt).strip()
        try:
            parsed_date = datetime.strptime(date_str, '%Y-%m-%d')
            return date_str, parsed_date
        except ValueError:
            print("Error: Please enter date in YYYY-MM-DD format (e.g., 2024-01-15)")

def get_date_range():
    # Get and validate date range from user
    begin_date_str, begin_date = get_date_input("Enter begin date (YYYY-MM-DD): ")

    while True:
        end_date_str, end_date = get_date_input("Enter end date (YYYY-MM-DD): ")

        if end_date >= begin_date:
            return begin_date_str, end_date_str
        else:
            print("Error: End date must be on or after the begin date")

def main():
    # Main application entry point
    print("=== Stock Data Visualization Tool ===")
    print("Alpha Vantage API Integration\n")

    try:
        # Get user inputs
        symbol = get_stock_symbol()
        chart_type = get_chart_type()
        time_series = get_time_series_function()
        begin_date, end_date = get_date_range()

        # Display collected information
        print(f"\n=== Configuration Summary ===")
        print(f"Stock Symbol: {symbol}")
        print(f"Chart Type: {chart_type}")
        print(f"Time Series: {time_series}")
        print(f"Date Range: {begin_date} to {end_date}")

        # Placeholder for future functionality
        print(f"\n[PLACEHOLDER] Fetching {time_series} data for {symbol}...")
        print(f"[PLACEHOLDER] Filtering data from {begin_date} to {end_date}...")
        print(f"[PLACEHOLDER] Generating {chart_type} chart...")
        print("[PLACEHOLDER] Opening chart in default browser...")

        print("\n Application completed successfully!")

    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()