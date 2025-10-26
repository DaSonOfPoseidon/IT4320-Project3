# Contributing to Stock Data Visualization Tool

Thank you for your interest in contributing! This document provides guidelines for development and testing.

## Development Setup

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/DaSonOfPoseidon/IT4320-Project3.git
cd IT4320-Project3

# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your Alpha Vantage API key
```

### 2. Configure Your Environment

Create a `.env` file with your API credentials:

```bash
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

Get a free API key from: https://www.alphavantage.co/support/#api-key

## Running Quality Checks Locally

Before pushing code, run the same checks that CI/CD will execute:

### Run All Tests

```bash
# Run tests with coverage
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_main.py

# Run tests matching a pattern
pytest -k "test_stock_symbol"
```

### Check Code Coverage

```bash
# Generate coverage report
pytest --cov=src --cov=main --cov-report=html

# Open HTML report in browser
# Windows
start htmlcov/index.html

# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html
```

### Run Linting (Pylint)

```bash
# Lint all Python files
pylint $(git ls-files '*.py')

# Lint specific file
pylint main.py

# Lint with specific rcfile
pylint --rcfile=.pylintrc main.py
```

### Run Code Formatting (Black)

```bash
# Check formatting (won't modify files)
black --check .

# Show what would change
black --diff .

# Auto-format all files
black .

# Format specific file
black main.py
```

### Run Type Checking (MyPy)

```bash
# Type check all files
mypy .

# Type check specific file
mypy main.py

# Install missing type stubs
mypy --install-types --non-interactive .
```

### Run All Checks at Once

```bash
# Quick validation before commit
black --check . && pylint $(git ls-files '*.py') && mypy . && pytest
```

## CI/CD Pipeline

Our GitHub Actions workflow runs automatically on:
- Every push to `main`, `develop`, or `phase-*` branches
- Every pull request to `main` or `develop`

### Pipeline Jobs

1. **Code Quality Checks** (warnings only, won't fail build)
   - Pylint: Code quality and style
   - Black: Code formatting
   - MyPy: Type checking

2. **Tests** (will fail build if issues found)
   - Pytest: Unit and integration tests
   - Coverage: Must maintain ≥70% code coverage

### Understanding CI Results

- ✅ **Green checkmark**: All tests passed, coverage met
- ⚠️ **Yellow warning**: Code quality issues (doesn't block merge)
- ❌ **Red X**: Tests failed or coverage too low (blocks merge)

## Writing Tests

### Test Organization

```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── test_main.py         # CLI tests
├── test_api_client.py   # API integration tests
├── test_data_processor.py
└── test_chart_generator.py
```

### Test Naming Conventions

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Example Test

```python
import pytest
from src.api_client import AlphaVantageClient

def test_api_client_initialization():
    """Test that API client initializes with valid key."""
    client = AlphaVantageClient(api_key="test_key")
    assert client.api_key == "test_key"

def test_invalid_symbol_raises_error():
    """Test that invalid symbol raises proper error."""
    client = AlphaVantageClient(api_key="test_key")
    with pytest.raises(InvalidSymbolError):
        client.fetch_stock_data("INVALID123", "TIME_SERIES_DAILY")
```

### Using Fixtures

```python
# In conftest.py
@pytest.fixture
def mock_api_client():
    """Provide mocked API client for tests."""
    return AlphaVantageClient(api_key="test_key", use_cache=False)

# In test file
def test_with_fixture(mock_api_client):
    """Test using the fixture."""
    assert mock_api_client.api_key == "test_key"
```

## Code Coverage Guidelines

### Target Coverage Levels

- **Overall**: 70-80% (enforced by CI/CD)
- **Critical paths** (API, validation): 85%+
- **UI/CLI functions**: 60%+ (harder to test)

### What to Test

✅ **Do test:**
- Business logic and calculations
- API integration and error handling
- Input validation
- Data processing functions
- Edge cases and error conditions

❌ **Don't waste time testing:**
- Third-party library internals
- Simple getters/setters
- Obvious pass-through functions

### Excluding Code from Coverage

```python
# Exclude specific lines
def debug_function():  # pragma: no cover
    print("Debug info")

# Exclude blocks
if __name__ == "__main__":  # pragma: no cover
    main()
```

## Branch Workflow

1. **Create feature branch** from `main`
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and test locally**
   ```bash
   # Run tests
   pytest

   # Check coverage
   pytest --cov=src --cov=main

   # Format code
   black .
   ```

3. **Push and create PR**
   ```bash
   git add .
   git commit -m "feat: add your feature"
   git push origin feature/your-feature-name
   ```

4. **Wait for CI/CD checks** before requesting review

## Common Issues

### Issue: Pylint fails with "Unable to import"

**Solution**: Ensure project dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Tests pass locally but fail in CI

**Solution**: Check for environment-specific issues
- Environment variables (use .env.example as template)
- File paths (use Path from pathlib)
- Python version differences

### Issue: Coverage report shows wrong percentage

**Solution**: Delete old coverage data
```bash
rm -rf .coverage htmlcov/ coverage.xml
pytest --cov=src --cov=main
```

### Issue: Black and existing code style conflict

**Solution**: Let Black win - it's more consistent
```bash
black .
git add -u
git commit -m "style: apply black formatting"
```

## Getting Help

- **Documentation**: See [README.md](README.md)
- **Issues**: Check [GitHub Issues](https://github.com/DaSonOfPoseidon/IT4320-Project3/issues)
- **Questions**: Open a new issue with the `question` label

## Code Style Guidelines

- **Line length**: 100 characters (configured in black/pylint)
- **Imports**: Sorted with isort (compatible with black)
- **Comments**: Use `#` for comments (per project style)
- **Docstrings**: Not required but encouraged for complex functions
- **Type hints**: Encouraged but not strictly enforced yet

## Pull Request Checklist

Before submitting a PR, ensure:

- [ ] All tests pass locally (`pytest`)
- [ ] Code coverage ≥70% (`pytest --cov`)
- [ ] Code formatted with black (`black .`)
- [ ] No pylint critical errors (`pylint $(git ls-files '*.py')`)
- [ ] Type hints added for new functions (optional)
- [ ] Documentation updated if needed
- [ ] `.env` file not committed (in .gitignore)
- [ ] No sensitive data in code
