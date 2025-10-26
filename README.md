# IT4320-Project3: Stock Data Visualization Tool

A command-line interface application for visualizing historical stock data using the Alpha Vantage API.

## Overview

This application allows users to:
- Query historical stock data for any publicly traded company
- Select from multiple chart types (line, candlestick, OHLC, volume)
- Choose different time series functions (daily, weekly, monthly, intraday)
- Filter data by custom date ranges
- Generate interactive charts that open in the default browser

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/DaSonOfPoseidon/IT4320-Project3.git
   cd IT4320-Project3
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key** 
   ```bash
   cp .env.example .env
   # Edit .env and add your Alpha Vantage API key
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## Project Structure

```
├── main.py                    # CLI entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variable template
├── tests/                    # Test suite
│   ├── __init__.py
│   └── test_api_client.py    # API client and cache tests
└── src/
    ├── __init__.py           # Package initialization
    ├── api_client.py         # Alpha Vantage API integration
    ├── cache_manager.py      # Response caching system
    ├── data_processor.py     # Date filtering and processing
    └── chart_generator.py    # Chart generation with Plotly
```

## Development Phases

- [x] **Phase 1**: Basic CLI skeleton
- [x] **Phase 2**: Alpha Vantage API integration with caching
- [ ] **Phase 3**: Complete user input system
- [ ] **Phase 4**: Date range filtering and data processing
- [ ] **Phase 5**: Interactive chart generation
- [ ] **Phase 6**: Polish and documentation

### Phase 2 Enhancements

Phase 2 has been completed with comprehensive API integration:

- **Alpha Vantage API Client**
  - Support for all 7 time series functions (daily, weekly, monthly, intraday)
  - Automatic API key management from environment variables
  - Pandas DataFrame output for easy data processing
  - Clean column names and datetime indexing

- **Intelligent Caching System**
  - Disk-based caching to minimize API calls (25 request/day limit)
  - 24-hour cache expiration (configurable)
  - Automatic cache validation and retrieval
  - Reduces API usage for repeated queries

- **Robust Error Handling**
  - Rate limit detection with clear user messaging
  - Invalid symbol detection and validation
  - Network error retry with exponential backoff (3 attempts)
  - Timeout handling with configurable limits

- **Intraday Support**
  - Automatic interval selection for intraday queries
  - 5 interval options (1min, 5min, 15min, 30min, 60min)
  - Smart prompting based on time series selection

- **Testing Suite**
  - 10 comprehensive tests (100% passing)
  - Mock-based testing for API calls
  - Cache manager validation tests
  - Error condition coverage

## Alpha Vantage API

This project uses the Alpha Vantage API for historical stock data.
- Free tier: 25 requests per day
- Get your API key: https://www.alphavantage.co/support/#api-key

## Team Members

- DaSonOfPoseidon
- 2
- 3
- 4

## License

Educational project for University of Missouri - Columbia IT4320 "Software Engineering"
