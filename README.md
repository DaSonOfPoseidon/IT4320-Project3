# IT4320-Project3: Stock Data Visualization Tool

[![CI/CD Pipeline](https://github.com/DaSonOfPoseidon/IT4320-Project3/actions/workflows/ci.yml/badge.svg)](https://github.com/DaSonOfPoseidon/IT4320-Project3/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line interface application for visualizing historical stock data using the Alpha Vantage API.

## Overview

This application allows users to:
- Query historical stock data for any publicly traded company
- Select from multiple chart types (line, candlestick, OHLC, volume)
- Choose different time series functions (daily, weekly, monthly, intraday)
- Filter data by custom date ranges
- Generate interactive charts that open in the default browser

## Setup Instructions

### For Users

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

### For Developers

For contributing to the project, additional setup is required:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Check code coverage
pytest --cov=src --cov=main --cov-report=html

# Format code
black .

# Lint code
pylint $(git ls-files '*.py')
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines.

## Project Structure

```
├── main.py                    # CLI entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variable template
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_input_validator.py   # Unit tests for validation
│   └── test_main_flow.py         # Integration tests
└── src/
    ├── __init__.py           # Package initialization
    ├── constants.py          # Configuration constants
    ├── input_validator.py    # Input validation utilities
    ├── api_client.py         # Alpha Vantage API integration
    ├── data_processor.py     # Date filtering and processing
    └── chart_generator.py    # Chart generation with Plotly
```

## Development Phases

- [x] **Phase 1**: Basic CLI skeleton - JK
- [ ] **Phase 2**: Alpha Vantage API integration
- [x] **Phase 3**: Complete user input system with enhanced validation - JK
- [ ] **Phase 4**: Date range filtering and data processing
- [ ] **Phase 5**: Interactive chart generation
- [ ] **Phase 6**: Finalize testing for previous modules
- [ ] **Phase 7**: Polish and documentation

### Phase 3 Enhancements

Phase 3 has been completed with comprehensive input validation:

- **Enhanced Stock Symbol Validation**
  - Format validation (1-5 letters forced to uppercase)
  - Helpful error messages with examples
  - Configurable retry limits

- **Intraday Interval Selection**
  - Automatically prompted for TIME_SERIES_INTRADAY
  - Five interval options (1min, 5min, 15min, 30min, 60min)
  - Smart conditional prompting

- **Advanced Date Validation**
  - Future date detection and rejection
  - Weekend/market closure warnings
  - Date range validation (max 20 years)
  - Leap year handling
  - Invalid calendar date detection

- **Environment Configuration Validation**
  - .env file existence check at startup
  - API key configuration validation
  - Clear setup instructions on failure

- **Robust Error Handling**
  - Maximum retry limits prevent infinite loops
  - Keyboard interrupt (Ctrl+C) handling at all input points
  - Consistent error message formatting
  - Retry attempt tracking

- **Testing Suite**
  - 59 comprehensive tests (100% passing)
  - Unit tests for all validators
  - Integration tests for complete user flows
  - Edge case coverage (leap years, weekends, boundaries)

## Testing

Run the comprehensive test suite:

```bash
# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_input_validator.py
```

**Test Coverage:**
- 59 tests covering all validation logic
- Unit tests for individual validators
- Integration tests for complete application flows
- Edge case and error condition testing

## Testing

This project uses automated testing with continuous integration via GitHub Actions.

### CI/CD Status

- ✅ **GitHub Actions configured** - Runs automatically on all pushes and PRs
- ⚠️ **Tests**: Will be enforced once test files are added (currently in development)
- ⚠️ **Code Quality**: Pylint, Black, and MyPy configured (warnings only, won't block merges)

### Running Tests Locally

```bash
# Run all tests (once tests are added)
pytest

# Run with coverage report
pytest --cov=src --cov=main

# Run specific test file
pytest tests/test_main.py

# Generate HTML coverage report
pytest --cov=src --cov=main --cov-report=html
open htmlcov/index.html  # View in browser
```

### Code Quality Checks

```bash
# Format code with Black
black .

# Lint with Pylint
pylint $(git ls-files '*.py')

# Type check with MyPy
mypy .
```

### Coverage Requirements

- **Minimum coverage**: 70%
- **Target coverage**: 70-80%
- Tests must pass before merging to main (after test implementation phase)

**Note:** The CI/CD pipeline is configured to gracefully handle the absence of tests during early development phases. Once test files are added to the `tests/` directory, coverage enforcement will automatically activate.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed testing guidelines.

## Alpha Vantage API

This project uses the Alpha Vantage API for historical stock data.
- Free tier: 25 requests per day
- Get your API key: https://www.alphavantage.co/support/#api-key

## Team Members

- Jackson K
- Supreet A
- Stephen B
- Jack H

## License

Educational project for University of Missouri - Columbia IT4320 "Software Engineering"
