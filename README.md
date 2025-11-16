# IT4320-Project3: Stock Data Visualization Tool

[![CI/CD Pipeline](https://github.com/DaSonOfPoseidon/IT4320-Project3/actions/workflows/ci.yml/badge.svg)](https://github.com/DaSonOfPoseidon/IT4320-Project3/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code Coverage](https://img.shields.io/badge/coverage-80%25-brightgreen.svg)](https://github.com/DaSonOfPoseidon/IT4320-Project3)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A web-based application for visualizing historical stock data using the Alpha Vantage API with intelligent caching, comprehensive input validation, and Docker deployment support.

## 🚀 Features

✅ **Complete & Working:**

- 🌐 **Web-Based Interface**: Modern Flask web application with intuitive forms
- 📊 **Multiple Chart Types**: Line charts, candlestick charts, OHLC bars, volume overlays
- 📈 **7 Time Series Functions**: Daily, weekly, monthly, intraday (with 5 interval options)
- 📋 **Stock Symbol Dropdown**: Pre-populated with 20 popular stocks for easy selection
- 🔍 **Comprehensive Input Validation**: Stock symbols, dates, date ranges with smart error messages
- 🌐 **Alpha Vantage API Integration**: Full support with automatic error handling
- 💾 **Intelligent Caching**: 24-hour disk cache to minimize API calls (25 request/day limit)
- ⚡ **Network Resilience**: Automatic retry with exponential backoff
- 📅 **Date Range Filtering**: Process and filter data based on user-specified date ranges
- 📈 **Interactive Chart Generation**: Plotly-powered HTML charts embedded in browser
- 🐳 **Docker Support**: Full containerization with Docker Compose for easy deployment
- 🧪 **50 Passing Tests**: Comprehensive test suite with 80% code coverage
- 🤖 **CI/CD Automation**: GitHub Actions with automated testing, linting, and PR reports

## 📋 Quick Start

### Prerequisites

- Docker and Docker Compose ([Get Docker](https://docs.docker.com/get-docker/))
- Alpha Vantage API key ([Get one free](https://www.alphavantage.co/support/#api-key))

### Running with Docker (Recommended)

1. **Clone the repository**

   ```bash
   git clone https://github.com/DaSonOfPoseidon/IT4320-Project3.git
   cd IT4320-Project3
   ```

2. **Configure API key**

   ```bash
   cp .env.example .env
   # Edit .env and add your Alpha Vantage API key:
   # ALPHA_VANTAGE_API_KEY=your_actual_key_here
   ```

3. **Build and run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

4. **Access the web application**

   Open your browser and navigate to: `http://localhost:5000`

5. **Stop the application**

   ```bash
   docker-compose down
   ```

## 🌐 Alternative: Running Locally with Flask

If you prefer not to use Docker, you can run the Flask application directly:

1. **Clone the repository** (if not already done)

   ```bash
   git clone https://github.com/DaSonOfPoseidon/IT4320-Project3.git
   cd IT4320-Project3
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API key**

   ```bash
   cp .env.example .env
   # Edit .env and add your Alpha Vantage API key
   ```

4. **Run the Flask application**

   ```bash
   python app.py
   ```

5. **Access the web interface**

   Open your browser and navigate to: `http://localhost:5000`

## 🐳 Advanced Docker Usage

### Using Docker Directly (Without Compose)

1. **Build the Docker image**

   ```bash
   docker build -t stock-chart-generator .
   ```

2. **Run the container**

   ```bash
   docker run -p 5000:5000 --env-file .env -v ./cache:/app/cache stock-chart-generator
   ```

3. **Access the web application**

   Open your browser and navigate to: `http://localhost:5000`

## ✨ Web Application Features

- 📋 **Stock Symbol Dropdown**: Pre-populated with 20 popular stocks for easy selection
- 🎨 **Interactive Forms**: Intuitive web interface for configuring chart parameters
- 📊 **Embedded Charts**: Charts display directly in the browser with full Plotly interactivity
- ⚠️ **Error Handling**: User-friendly error pages with troubleshooting tips
- 💾 **Persistent Cache**: Cache is stored in a Docker volume for efficiency across restarts
- 🔄 **Customizable Symbols**: Modify stock symbols by editing `stock_symbols.json`
- 📱 **Responsive Design**: Works on desktop and mobile browsers

## 🏗️ Project Structure

```
IT4320-Project3/
├── app.py                        # Flask web application entry point
├── stock_symbols.json            # Stock symbols for dropdown menu
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
├── .env.example                  # Environment variable template
├── Dockerfile                    # Docker container configuration
├── docker-compose.yml            # Docker Compose orchestration
├── .dockerignore                 # Files excluded from Docker image
├── .coveragerc                   # Coverage configuration
├── pytest.ini                    # Pytest configuration
├── pyproject.toml                # Project metadata and tool configs
│
├── templates/                    # Flask HTML templates
│   ├── index.html                # Main form page
│   ├── result.html               # Chart display page
│   └── error.html                # Error page with troubleshooting
│
├── .github/
│   └── workflows/
│       └── ci.yml                # CI/CD pipeline configuration
│
├── src/                          # Core business logic package
│   ├── __init__.py               # Package initialization
│   ├── constants.py              # Configuration constants (chart types, time series)
│   ├── input_validator.py        # Input validation utilities
│   ├── api_client.py             # Alpha Vantage API client with retry logic
│   ├── cache_manager.py          # Intelligent response caching system
│   ├── data_processor.py         # Data filtering and processing
│   └── chart_generator.py        # Chart generation with Plotly
│
└── tests/                        # Test suite (50 tests, 80% coverage)
    ├── __init__.py
    ├── test_input_validator.py   # 33 unit tests for validation logic
    └── test_api_client.py        # 16 tests for API client and caching
```

## 🎯 Development Phases

| Phase | Status | Description | Lead |
|-------|--------|-------------|------|
| **Phase 1** | ✅ Complete | Project setup and architecture | JK |
| **Phase 2** | ✅ Complete | Alpha Vantage API integration with caching | JK |
| **Phase 3** | ✅ Complete | Enhanced input validation and error handling | JK |
| **Phase 4** | ✅ Complete | Date range filtering and data processing | SA |
| **Phase 5** | ✅ Complete | Interactive chart generation with Plotly | SA |
| **Phase 6** | ✅ Complete | Web interface and Docker deployment | Team |

### ✨ Completed Features

#### 🌐 Web Interface

- Modern Flask web application with intuitive form-based input
- Stock symbol dropdown pre-populated with popular stocks
- Configuration form with date pickers and dropdown menus
- User-friendly error pages with troubleshooting guidance
- Embedded interactive Plotly charts in result pages

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

- **50 Passing Tests** across 2 test files
- **80% Code Coverage** (exceeds 70% minimum requirement)
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

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov=app --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=src --cov=app --cov-report=html
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
| `src/cache_manager.py` | 82 | 93% | Cache system |
| `src/input_validator.py` | 87 | 83% | Input validation |
| `src/api_client.py` | 110 | 68% | API integration |
| **TOTAL** | **290** | **80%** | ✅ Exceeds 70% requirement |

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

- ✅ Runs 50 tests across Python 3.9, 3.10, 3.11
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
  - Comprehensive test suite development (50 tests with 80% coverage)
  - README documentation and project structure
  - CI/CD pipeline configuration and GitHub Actions workflows
- Contributors and reviewers

---

**Project Status**: ✅ **PROJECT COMPLETE** - Web Application with Docker | 50 Tests Passing | 80% Coverage
