.PHONY: help install install-dev test test-verbose test-coverage lint format type-check clean build publish-test publish examples pre-commit security

help:  ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install package
	pip install -e .

install-dev:  ## Install package with development dependencies
	pip install -e ".[dev]"
	pre-commit install

test:  ## Run tests
	pytest

test-verbose:  ## Run tests with verbose output
	pytest -v

test-coverage:  ## Run tests with coverage report
	pytest --cov=src --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

lint:  ## Check code style and linting
	@echo "Checking with ruff..."
	ruff check src tests
	@echo "Checking with black..."
	black --check src tests

format:  ## Format code with black and ruff
	@echo "Formatting with black..."
	black src tests
	@echo "Auto-fixing with ruff..."
	ruff check --fix src tests
	@echo "Sorting imports with isort..."
	isort src tests

type-check:  ## Run type checking with mypy
	mypy src

security:  ## Run security checks
	@echo "Running bandit..."
	bandit -r src -c pyproject.toml
	@echo "Checking dependencies with safety..."
	safety check --json || true

pre-commit:  ## Run pre-commit hooks on all files
	pre-commit run --all-files

clean:  ## Clean build artifacts and cache files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:  ## Build distribution packages
	python -m build

publish-test: clean build  ## Publish to TestPyPI
	python -m twine upload --repository testpypi dist/*

publish: clean build  ## Publish to PyPI (production)
	python -m twine upload dist/*

examples:  ## Run all example scripts
	@echo "Running schedule management example..."
	python examples/schedule_management.py
	@echo ""
	@echo "Running data range analysis example..."
	python examples/data_range_analysis.py
	@echo ""
	@echo "Running temperature monitoring example..."
	python examples/temperature_monitoring.py

ci:  ## Run all CI checks locally
	@echo "Running CI checks locally..."
	@make format
	@make lint
	@make type-check
	@make test-coverage
	@make security
	@make examples
	@echo "✅ All CI checks passed!"

init:  ## Initialize development environment
	@echo "Initializing development environment..."
	python -m venv venv
	@echo "Virtual environment created. Activate it with:"
	@echo "  source venv/bin/activate  (on Unix/macOS)"
	@echo "  venv\\Scripts\\activate  (on Windows)"
	@echo ""
	@echo "Then run: make install-dev"

readme:  ## Validate README
	python -m readme_renderer README.md -o /tmp/README.html
	@echo "✅ README is valid"

all: format lint type-check test  ## Run format, lint, type-check, and test
	@echo "✅ All checks passed!"