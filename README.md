# IT4320-Project3: Stock Data Visualization Tool

[![CI/CD Pipeline](https://github.com/DaSonOfPoseidon/IT4320-Project3/actions/workflows/ci.yml/badge.svg)](https://github.com/DaSonOfPoseidon/IT4320-Project3/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code Coverage](https://img.shields.io/badge/coverage-75%25-brightgreen.svg)](https://github.com/DaSonOfPoseidon/IT4320-Project3)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line interface application for visualizing historical stock data using the Alpha Vantage API with intelligent caching, comprehensive input validation, and automated testing.

## 🚀 Features

✅ **Complete & Working:**

- 📊 **Multiple Chart Types**: Line charts, candlestick charts, OHLC bars, volume overlays
- 📈 **7 Time Series Functions**: Daily, weekly, monthly, intraday (with 5 interval options)
- 🔍 **Comprehensive Input Validation**: Stock symbols, dates, date ranges with smart error messages
- 🌐 **Alpha Vantage API Integration**: Full support with automatic error handling
- 💾 **Intelligent Caching**: 24-hour disk cache to minimize API calls (25 request/day limit)
- ⚡ **Network Resilience**: Automatic retry with exponential backoff
- 🧪 **75 Passing Tests**: Comprehensive test suite with 75% code coverage
- 🤖 **CI/CD Automation**: GitHub Actions with automated testing, linting, and PR reports

🚧 **In Progress:**

- Phase 4: Date range filtering and data processing
- Phase 5: Interactive chart generation

## 📋 Quick Start

### Prerequisites

- Python 3.9 or higher
- Alpha Vantage API key ([Get one free](https://www.alphavantage.co/support/#api-key))

### Installation

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
   # Edit .env and add your Alpha Vantage API key:
   # ALPHA_VANTAGE_API_KEY=your_actual_key_here
   ```

4. **Run the application**

   ```bash
   python main.py
   ```

## 🏗️ Project Structure

```
IT4320-Project3/
├── main.py                       # CLI entry point with main application flow
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
├── .env.example                  # Environment variable template
├── .coveragerc                   # Coverage configuration
├── pytest.ini                    # Pytest configuration
├── pyproject.toml                # Project metadata and tool configs
│
├── .github/
│   └── workflows/
│       └── ci.yml                # CI/CD pipeline configuration
│
├── src/                          # Source code package
│   ├── __init__.py               # Package initialization
│   ├── constants.py              # Configuration constants (chart types, time series)
│   ├── input_validator.py        # Input validation utilities with retry logic
│   ├── api_client.py             # Alpha Vantage API client
│   ├── cache_manager.py          # Intelligent response caching system
│   ├── data_processor.py         # Data filtering and processing (Phase 4)
│   └── chart_generator.py        # Chart generation with Plotly (Phase 5)
│
└── tests/                        # Test suite (75 tests, 75% coverage)
    ├── __init__.py
    ├── test_input_validator.py   # 33 unit tests for validation logic
    ├── test_api_client.py        # 16 tests for API client and caching
    └── test_main_flow.py          # 26 integration tests for user flows
```

## 🎯 Development Phases

| Phase | Status | Description | Lead |
|-------|--------|-------------|------|
| **Phase 1** | ✅ Complete | Basic CLI skeleton and menu system | JK |
| **Phase 2** | ✅ Complete | Alpha Vantage API integration with caching | JK |
| **Phase 3** | ✅ Complete | Enhanced input validation and error handling | JK |
| **Phase 4** | 🚧 In Progress | Date range filtering and data processing | - |
| **Phase 5** | 📋 Planned | Interactive chart generation with Plotly | - |
| **Phase 6** | 📋 Planned | Comprehensive testing for Phase 4-5 | - |
| **Phase 7** | 📋 Planned | Polish, documentation, and final delivery | - |

### ✨ Completed Features (Phases 1-3)

#### 🎨 User Interface

- Interactive CLI with clear prompts and instructions
- Configuration summary display before data fetching
- Keyboard interrupt (Ctrl+C) handling at all input points
- Helpful error messages with retry attempt tracking

#### 🔐 Input Validation

- **Stock Symbols**: 1-5 uppercase letters, helpful error messages with examples
- **Chart Types**: 4 options (line, candlestick, OHLC, volume) with descriptions
- **Time Series**: 7 Alpha Vantage functions with automatic interval selection
- **Intraday Intervals**: 5 options (1min, 5min, 15min, 30min, 60min)
- **Date Validation**:
  - Future date detection and rejection
  - Weekend/market closure warnings
  - Invalid calendar dates (Feb 30, Month 13, etc.)
  - Leap year support
  - Date range validation (max 20 years to prevent API abuse)
  - Order validation (end date must be after begin date)

#### 🌐 API Integration

- **Alpha Vantage Client**: Support for all 7 time series functions
- **Smart Caching**: 24-hour disk cache with automatic expiration
- **Error Handling**:
  - Rate limit detection (25 requests/day limit)
  - Invalid symbol detection
  - Network error retry with exponential backoff (3 attempts)
  - Timeout handling (10s default)
- **Data Processing**: Clean DataFrame output with datetime indexing

#### 🧪 Testing & Quality

- **75 Passing Tests** across 3 test files
- **75% Code Coverage** (exceeds 70% minimum requirement)
- **GitHub Actions CI/CD**:
  - Automated testing on Python 3.9, 3.10, 3.11
  - Code quality checks (Pylint, Black, MyPy)
  - Coverage reporting with PR comments
  - Merge conflict detection
  - Automated code quality reports

## 🧪 Testing

### Running Tests Locally

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all 75 tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov=main --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=src --cov=main --cov-report=html
open htmlcov/index.html  # View in browser

# Run specific test file
pytest tests/test_input_validator.py
pytest tests/test_api_client.py
pytest tests/test_main_flow.py
```

### Test Coverage Breakdown

| Module | Statements | Coverage | Notes |
|--------|------------|----------|-------|
| `src/constants.py` | 11 | 100% | Configuration constants |
| `src/cache_manager.py` | 83 | 93% | Cache system |
| `src/input_validator.py` | 87 | 83% | Input validation |
| `src/api_client.py` | 111 | 69% | API integration |
| `main.py` | 202 | 67% | Application flow |
| **TOTAL** | **496** | **75%** | ✅ Exceeds 70% requirement |

### Code Quality Checks

```bash
# Format code with Black
black .

# Lint with Pylint (currently rated 8.42/10)
pylint $(git ls-files '*.py')

# Type check with MyPy
mypy . --install-types --non-interactive
```

### CI/CD Pipeline

Every push and pull request automatically:

- ✅ Runs 75 tests across Python 3.9, 3.10, 3.11
- 📊 Generates coverage reports (artifacts downloadable)
- 🤖 Posts automated PR comments with:
  - Code quality metrics (Pylint score, Black formatting, MyPy results)
  - Coverage percentage and trends
  - Merge conflict status
- 📥 Creates downloadable artifacts with detailed linter reports

## 🔧 Development

### For Contributors

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines.

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Create a new feature branch
git checkout -b feature/your-feature-name

# Make changes and run tests
pytest

# Format and lint before committing
black .
pylint $(git ls-files '*.py')

# Commit with descriptive message
git commit -m "feat: add new feature"

# Push and create PR
git push origin feature/your-feature-name
```

### Development Workflow

1. **Create feature branch** from `main`
2. **Write tests first** (TDD approach recommended)
3. **Implement feature** with clean, documented code
4. **Run tests locally** to ensure they pass
5. **Format code** with Black
6. **Create Pull Request** - CI will automatically:
   - Run all tests
   - Check code quality
   - Report coverage
   - Check for merge conflicts

## 📚 API Reference

### Alpha Vantage API

This project uses the [Alpha Vantage API](https://www.alphavantage.co/) for historical stock data.

- **Free Tier**: 25 requests per day
- **Caching**: 24-hour cache reduces API usage
- **Get API Key**: https://www.alphavantage.co/support/#api-key

**Supported Time Series Functions:**

1. `TIME_SERIES_DAILY` - Daily time series data
2. `TIME_SERIES_DAILY_ADJUSTED` - Daily with split/dividend adjustments
3. `TIME_SERIES_WEEKLY` - Weekly time series data
4. `TIME_SERIES_WEEKLY_ADJUSTED` - Weekly with adjustments
5. `TIME_SERIES_MONTHLY` - Monthly time series data
6. `TIME_SERIES_MONTHLY_ADJUSTED` - Monthly with adjustments
7. `TIME_SERIES_INTRADAY` - Intraday data (requires interval: 1min, 5min, 15min, 30min, 60min)

## 🎓 Team Members

- **Jackson K** - Developer 
- **Supreet A** - Developer
- **Stephen B** - Documentation
- **Jack H** - Scrum Master

## 📄 License

Educational project for University of Missouri - Columbia
**IT4320 "Software Engineering"**
MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **Alpha Vantage** for providing the stock data API
- **University of Missouri - Columbia** IT4320 Course Staff
- **Claude (Anthropic)** for assistance with:
  - Comprehensive test suite development (75 tests with 75% coverage)
  - README documentation and project structure
  - CI/CD pipeline configuration and GitHub Actions workflows
- Contributors and reviewers

---

**Project Status**: ✅ Phases 1-3 Complete | 🚧 Phase 4 In Progress | 75 Tests Passing | 75% Coverage
