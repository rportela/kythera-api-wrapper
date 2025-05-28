@echo off
REM Development helper script for kythera-kdx on Windows

if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="install-dev" goto install-dev
if "%1"=="test" goto test
if "%1"=="test-cov" goto test-cov
if "%1"=="lint" goto lint
if "%1"=="format" goto format
if "%1"=="type-check" goto type-check
if "%1"=="clean" goto clean
if "%1"=="build" goto build
if "%1"=="" goto help

echo Unknown command: %1
goto help

:help
echo Available commands:
echo   install      Install package for production
echo   install-dev  Install package with development dependencies
echo   test         Run tests
echo   test-cov     Run tests with coverage
echo   lint         Run linting (flake8)
echo   format       Format code with black and isort
echo   type-check   Run type checking with mypy
echo   clean        Clean build artifacts
echo   build        Build package
goto end

:install
pip install -e .
goto end

:install-dev
pip install -r requirements-dev.txt
pip install -e .
pre-commit install
goto end

:test
pytest
goto end

:test-cov
pytest --cov=kythera_kdx --cov-report=term-missing --cov-report=html
goto end

:lint
flake8 src/ tests/
goto end

:format
black src/ tests/
isort src/ tests/
goto end

:type-check
mypy src/
goto end

:clean
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.egg-info rmdir /s /q *.egg-info
if exist .pytest_cache rmdir /s /q .pytest_cache
if exist .coverage del .coverage
if exist htmlcov rmdir /s /q htmlcov
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
for /r . %%f in (*.pyc) do @if exist "%%f" del "%%f"
goto end

:build
call :clean
python -m build
goto end

:end
