# Development Setup Guide

This guide will help you set up your development environment for contributing to the Interval Arithmetic library.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- git
- (Optional) make (for using Makefile commands)

## Quick Setup

### Using Make (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/interval-arithmetic.git
cd interval-arithmetic

# Initialize development environment
make init

# Activate virtual environment
source venv/bin/activate  # On Unix/macOS
# or
venv\Scripts\activate  # On Windows

# Install development dependencies
make install-dev

# Run tests to verify setup
make test
```

### Manual Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/interval-arithmetic.git
cd interval-arithmetic

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Unix/macOS
# or
venv\Scripts\activate  # On Windows

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

## Verify Installation

Run these commands to verify everything is set up correctly:

```bash
# Run tests
make test
# or
pytest

# Check code style
make lint
# or
black --check src tests && ruff check src tests

# Run type checker
make type-check
# or
mypy src

# Run examples
make examples
# or
python examples/schedule_management.py
```

If all commands succeed, your development environment is ready! ✅

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Your Changes

Edit files in `src/` or `tests/`

### 3. Run Quality Checks

```bash
# Format code
make format

# Run all checks
make all

# Or run individually:
make lint        # Check code style
make type-check  # Type checking
make test        # Run tests
```

### 4. Commit Your Changes

Pre-commit hooks will run automatically:

```bash
git add .
git commit -m "feat: add new feature"
```

If pre-commit hooks fail, fix the issues and commit again.

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Available Make Commands

View all available commands:

```bash
make help
```

Common commands:

| Command | Description |
|---------|-------------|
| `make install` | Install package |
| `make install-dev` | Install with dev dependencies |
| `make test` | Run tests |
| `make test-coverage` | Run tests with coverage report |
| `make lint` | Check code style |
| `make format` | Auto-format code |
| `make type-check` | Run type checker |
| `make security` | Run security checks |
| `make examples` | Run all examples |
| `make clean` | Clean build artifacts |
| `make ci` | Run all CI checks locally |
| `make all` | Format, lint, type-check, and test |

## Running Tests

### All Tests

```bash
make test
# or
pytest
```

### With Coverage

```bash
make test-coverage
# or
pytest --cov=src --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

### Specific Test File

```bash
pytest tests/test_integration.py
```

### Specific Test Function

```bash
pytest tests/test_integration.py::TestScheduleManagementWorkflow::test_find_available_time_slots
```

### Watch Mode (requires pytest-watch)

```bash
pip install pytest-watch
ptw
```

## Code Quality Tools

### Black (Code Formatting)

```bash
# Check formatting
black --check src tests

# Auto-format
make format
# or
black src tests
```

### Ruff (Linting)

```bash
# Check for issues
ruff check src tests

# Auto-fix issues
ruff check --fix src tests
```

### Mypy (Type Checking)

```bash
make type-check
# or
mypy src
```

### Pre-commit Hooks

Pre-commit hooks run automatically on `git commit`. To run manually:

```bash
make pre-commit
# or
pre-commit run --all-files
```

## Security Checks

### Bandit (Security Linter)

```bash
bandit -r src -c pyproject.toml
```

### Safety (Dependency Checker)

```bash
safety check
```

### Run All Security Checks

```bash
make security
```

## Building and Publishing

### Build Distribution

```bash
make build
# or
python -m build
```

Creates `dist/` directory with wheel and source distribution.

### Test Distribution

```bash
# Install from local build
pip install dist/*.whl

# Test it works
python -c "from src.intervals import Interval; print(Interval.point(5))"
```

### Publish to TestPyPI

```bash
make publish-test
```

Requires TestPyPI API token in `~/.pypirc` or as environment variable.

### Publish to PyPI

```bash
make publish
```

⚠️ **Warning**: This publishes to production PyPI. Only maintainers should do this.

## IDE Setup

### VS Code

Install recommended extensions:
- Python
- Pylance
- Python Test Explorer

Settings (`.vscode/settings.json`):

```json
{
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

### PyCharm

1. Open project in PyCharm
2. Set interpreter to `venv/bin/python`
3. Enable pytest: Settings → Tools → Python Integrated Tools → Testing → pytest
4. Configure Black: Settings → Tools → Black
5. Configure Ruff: Settings → Tools → External Tools

## Troubleshooting

### Import Errors

If you get import errors, make sure you've installed in development mode:

```bash
pip install -e ".[dev]"
```

### Pre-commit Hook Fails

If pre-commit hooks fail, you can:

1. Fix the issues manually
2. Let pre-commit auto-fix: `pre-commit run --all-files`
3. Skip hooks (not recommended): `git commit --no-verify`

### Test Failures

If tests fail:

1. Check if you have the latest dependencies: `pip install -e ".[dev]" --upgrade`
2. Clear cache: `make clean`
3. Run specific failing test: `pytest tests/test_file.py::test_name -v`

### Type Checking Errors

If mypy reports errors:

1. Check if type hints are correct
2. Update mypy: `pip install mypy --upgrade`
3. Check `pyproject.toml` for mypy configuration

## Getting Help

- 📖 Read [CONTRIBUTING.md](CONTRIBUTING.md)
- 💬 Ask in [Discussions](https://github.com/yourusername/interval-arithmetic/discussions)
- 🐛 Report bugs in [Issues](https://github.com/yourusername/interval-arithmetic/issues)
- 📧 Contact maintainers: your.email@example.com

## Next Steps

1. ✅ Verify your setup with `make test`
2. 📖 Read [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
3. 🎯 Find an issue to work on or propose a new feature
4. 💻 Start coding!

Happy coding! 🚀