@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    HealthFirst AI Integration Setup
echo ========================================
echo.

:: Check if virtual environment exists
if not exist ".venv" (
    echo [1/5] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

:: Activate virtual environment
echo [2/5] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activated

:: Install dependencies
echo [3/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed

:: Initialize AI system
echo [4/5] Initializing AI Diagnosis System...
python init_ai.py
if errorlevel 1 (
    echo ❌ Failed to initialize AI system
    echo.
    echo Please check:
    echo 1. AI data files exist in ai_data/ folder
    echo 2. All dependencies are installed
    echo 3. Python version is 3.8 or higher
    echo.
    pause
    exit /b 1
)
echo ✅ AI system initialized successfully

:: Create admin user if needed
echo [5/5] Setting up admin user...
python fix_admin.py
if errorlevel 1 (
    echo ⚠️  Warning: Failed to setup admin user
    echo    You can create admin manually later
) else (
    echo ✅ Admin user setup completed
)

echo.
echo ========================================
echo    🎉 Setup Complete!
echo ========================================
echo.
echo HealthFirst AI is ready to run!
echo.
echo Default admin credentials:
echo   Email: admin@healthfirst.com
echo   Password: admin123
echo.
echo Starting HealthFirst website...
echo.
echo Press Ctrl+C to stop the server
echo.

:: Start the Flask application
python run.py

pause
