@echo off
echo ================================================
echo        Google Forms MCQ Generator
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show requests >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if credentials exist
if not exist "credentials.json" (
    echo ERROR: credentials.json not found!
    echo Please download OAuth credentials from Google Cloud Console
    echo and save as 'credentials.json' in this directory
    pause
    exit /b 1
)

echo.
echo Dependencies OK! Starting application...
echo.

REM Run the main application
if "%1"=="" (
    echo Running with default example file...
    python main.py
) else (
    echo Running with file: %1
    python main.py %*
)

echo.
echo ================================================
echo           Form Creation Complete!
echo ================================================
pause
