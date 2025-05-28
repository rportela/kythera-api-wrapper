# Makefile for kythera-kdx development

.PHONY: help install install-dev test test-cov lint format type-check clean build upload docs

help:
	@echo "Available commands:"
	@echo "  install      Install package for production"
	@echo "  install-dev  Install package with development dependencies"
	@echo "  test         Run tests"
	@echo "  test-cov     Run tests with coverage"
	@echo "  lint         Run linting (flake8)"
	@echo "  format       Format code with black and isort"
	@echo "  type-check   Run type checking with mypy"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build package"
	@echo "  upload       Upload to PyPI (requires authentication)"
	@echo "  docs         Generate documentation"

install:
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .
	pre-commit install

test:
	pytest

test-cov:
	pytest --cov=kythera_kdx --cov-report=term-missing --cov-report=html

lint:
	flake8 src/ tests/

format:
	black src/ tests/
	isort src/ tests/

type-check:
	mypy src/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

upload: build
	python -m twine upload dist/*

docs:
	@echo "Documentation generation not yet implemented"
