@echo off
echo ===================================================
echo 🚀 Starting AlgoSync Multiagent Debugger
echo ===================================================
echo.

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b
)

:: Check for Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed or not in PATH.
    pause
    exit /b
)

echo [1/3] Installing/Verifying Backend Dependencies...
cd backend
call pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [WARNING] Some dependencies might have failed. Attempting to continue...
)

echo.
echo [2/3] Starting Backend Server (Port 5000)...
start "AlgoSync Backend" cmd /k "python app.py"

echo.
echo [3/3] Starting Frontend Server (Port 5173)...
cd ../frontend
call npm install
start "AlgoSync Frontend" cmd /k "npm run dev"

echo.
echo ===================================================
echo ✅ System Started!
echo Frontend: http://localhost:5173
echo Backend: http://localhost:5000
echo.
echo Press any key to close this launcher (Servers will keep running)...
pause
