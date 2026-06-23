@echo off
echo Starting CareerConnect...

echo Starting Backend API Server (Port 8000)...
start cmd /k "cd backend && uvicorn main:app --reload --port 8000"

echo Starting Frontend Server (Port 3000)...
start cmd /k "cd frontend && python -m http.server 3000"

echo ==============================================
echo Servers have been launched in separate windows!
echo ==============================================
echo Frontend is available at: http://localhost:3000
echo Backend API is available at: http://localhost:8000
echo ==============================================
pause
