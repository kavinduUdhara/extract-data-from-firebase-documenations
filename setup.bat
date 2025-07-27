@echo off
REM Setup script for Firebase Documentation Extractor (Windows)

echo 🔥 Firebase Documentation Extractor Setup
echo ==========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.7+ first.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python found: %PYTHON_VERSION%

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv .venv

REM Activate virtual environment
echo ✅ Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

echo.
echo 🎉 Setup complete!
echo.
echo To use the tool:
echo 1. Activate the virtual environment:
echo    .venv\Scripts\activate.bat
echo 2. Run the extractor:
echo    python firebase_docs_extractor.py "^<FIREBASE_URL^>"
echo.
echo Example:
echo    python firebase_docs_extractor.py "https://firebase.google.com/docs/ai-logic/get-started?api=vertex"
echo.
pause
