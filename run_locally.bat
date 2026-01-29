@echo off
title AlgoSync Multiagent Debugger
color 0A

echo.
echo  ╔═══════════════════════════════════════════════════════════╗
echo  ║          AlgoSync - Multiagent Code Debugger              ║
echo  ║              Easy Launcher v2.0                           ║
echo  ╚═══════════════════════════════════════════════════════════╝
echo.

:menu
echo  Choose an option:
echo.
echo  [1] Start Both Servers (Backend + Frontend)
echo  [2] Start Backend Only (Port 5000)
echo  [3] Start Frontend Only (Port 5173)
echo  [4] Install Dependencies
echo  [5] Open Application in Browser
echo  [6] Exit
echo.
set /p choice="Enter choice (1-6): "

if "%choice%"=="1" goto start_both
if "%choice%"=="2" goto start_backend
if "%choice%"=="3" goto start_frontend
if "%choice%"=="4" goto install_deps
if "%choice%"=="5" goto open_browser
if "%choice%"=="6" goto end

echo Invalid choice. Please try again.
goto menu

:start_both
echo.
echo [Starting Backend...]
cd backend
start "AlgoSync Backend" cmd /k "python app.py"
cd ..
echo [Starting Frontend...]
cd frontend
start "AlgoSync Frontend" cmd /k "npm run dev"
cd ..
echo.
echo ✅ Both servers started!
echo    Frontend: http://localhost:5173
echo    Backend:  http://localhost:5000
echo.
pause
goto menu

:start_backend
echo.
echo [Starting Backend Server...]
cd backend
start "AlgoSync Backend" cmd /k "python app.py"
cd ..
echo ✅ Backend started on http://localhost:5000
pause
goto menu

:start_frontend
echo.
echo [Starting Frontend Server...]
cd frontend
start "AlgoSync Frontend" cmd /k "npm run dev"
cd ..
echo ✅ Frontend started on http://localhost:5173
pause
goto menu

:install_deps
echo.
echo [Installing Backend Dependencies...]
cd backend
pip install -r requirements.txt
cd ..
echo.
echo [Installing Frontend Dependencies...]
cd frontend
npm install
cd ..
echo.
echo ✅ All dependencies installed!
pause
goto menu

:open_browser
echo.
echo Opening http://localhost:5173 in browser...
start http://localhost:5173
goto menu

:end
echo.
echo Goodbye!
exit /b
