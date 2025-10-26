# /usr/bin/env python3
# Constants for Stock Data Visualization CLI Application
# Centralized configuration for chart types, time series, and intervals

# Chart type configurations
CHART_TYPES = {
    '1': {
        'key': 'line',
        'display': 'Line Chart (Close Price)',
        'description': 'Simple line chart showing closing prices over time'
    },
    '2': {
        'key': 'candlestick',
        'display': 'Candlestick Chart',
        'description': 'Traditional candlestick chart showing OHLC data'
    },
    '3': {
        'key': 'ohlc',
        'display': 'OHLC Bar Chart',
        'description': 'Bar chart showing Open, High, Low, Close prices'
    },
    '4': {
        'key': 'volume',
        'display': 'Volume Overlay Chart',
        'description': 'Price chart with trading volume overlay'
    }
}

# Time series function configurations
TIME_SERIES_FUNCTIONS = {
    '1': {
        'key': 'TIME_SERIES_DAILY',
        'display': 'Daily (TIME_SERIES_DAILY)',
        'description': 'Daily time series (date, daily open, daily high, daily low, daily close, daily volume)',
        'requires_interval': False
    },
    '2': {
        'key': 'TIME_SERIES_DAILY_ADJUSTED',
        'display': 'Daily Adjusted (TIME_SERIES_DAILY_ADJUSTED)',
        'description': 'Daily time series with split/dividend adjustments',
        'requires_interval': False
    },
    '3': {
        'key': 'TIME_SERIES_WEEKLY',
        'display': 'Weekly (TIME_SERIES_WEEKLY)',
        'description': 'Weekly time series (last trading day of each week)',
        'requires_interval': False
    },
    '4': {
        'key': 'TIME_SERIES_WEEKLY_ADJUSTED',
        'display': 'Weekly Adjusted (TIME_SERIES_WEEKLY_ADJUSTED)',
        'description': 'Weekly time series with split/dividend adjustments',
        'requires_interval': False
    },
    '5': {
        'key': 'TIME_SERIES_MONTHLY',
        'display': 'Monthly (TIME_SERIES_MONTHLY)',
        'description': 'Monthly time series (last trading day of each month)',
        'requires_interval': False
    },
    '6': {
        'key': 'TIME_SERIES_MONTHLY_ADJUSTED',
        'display': 'Monthly Adjusted (TIME_SERIES_MONTHLY_ADJUSTED)',
        'description': 'Monthly time series with split/dividend adjustments',
        'requires_interval': False
    },
    '7': {
        'key': 'TIME_SERIES_INTRADAY',
        'display': 'Intraday (TIME_SERIES_INTRADAY)',
        'description': 'Intraday time series - requires interval selection',
        'requires_interval': True
    }
}

# Intraday interval configurations
INTRADAY_INTERVALS = {
    '1': {
        'key': '1min',
        'display': '1 minute',
        'description': 'Most granular data, ideal for day trading'
    },
    '2': {
        'key': '5min',
        'display': '5 minutes',
        'description': 'Short-term intraday analysis'
    },
    '3': {
        'key': '15min',
        'display': '15 minutes',
        'description': 'Medium-term intraday analysis'
    },
    '4': {
        'key': '30min',
        'display': '30 minutes',
        'description': 'Longer-term intraday analysis'
    },
    '5': {
        'key': '60min',
        'display': '60 minutes (1 hour)',
        'description': 'Hourly data points throughout trading day'
    }
}

# Validation constraints
SYMBOL_MIN_LENGTH = 1
SYMBOL_MAX_LENGTH = 5
MAX_SYMBOL_INPUT_RETRIES = 3
MAX_CHOICE_INPUT_RETRIES = 5
MAX_DATE_INPUT_RETRIES = 5
MAX_DATE_RANGE_YEARS = 20

# Date validation messages
DATE_FORMAT = '%Y-%m-%d'
DATE_FORMAT_DISPLAY = 'YYYY-MM-DD'
