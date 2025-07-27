@echo off
REM Firebase Documentation Extractor - Windows Batch Script with Language Support
REM Usage: extract_docs.bat "URL" [languages]
REM Example: extract_docs.bat "https://firebase.google.com/docs/ai-logic/get-started?api=vertex" "swift web"

if "%1"=="" (
    echo Usage: extract_docs.bat "URL" [languages]
    echo.
    echo Examples:
    echo   extract_docs.bat "https://firebase.google.com/docs/ai-logic/get-started?api=vertex"
    echo   extract_docs.bat "https://firebase.google.com/docs/ai-logic/get-started?api=vertex" "swift web"
    echo   extract_docs.bat "https://firebase.google.com/docs/auth" "kotlin java"
    echo.
    echo Supported languages: swift, kotlin, java, web, dart, unity, python, go, php, ruby, node
    exit /b 1
)

echo Extracting Firebase documentation from: %1

if "%2"=="" (
    "F:\repos\extract-data-from-firebase-documenations\.venv\Scripts\python.exe" firebase_docs_extractor.py %1
) else (
    "F:\repos\extract-data-from-firebase-documenations\.venv\Scripts\python.exe" firebase_docs_extractor.py %1 --languages %2
)

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Documentation extracted successfully!
) else (
    echo.
    echo ❌ Failed to extract documentation
)

pause
