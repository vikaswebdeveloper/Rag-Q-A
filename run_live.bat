@echo off
title RAG Q&A Library - Live Server Launcher
echo ======================================================================
echo          LAUNCHING RAG Q&A DIGITAL LIBRARY (LIVE SYSTEM)             
echo ======================================================================
echo.

cd /d "%~dp0"

echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000 ...
start "RAG Backend (FastAPI)" cmd /k "cd backend && ..\.venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8000 --reload"

echo [2/2] Starting Next.js Frontend on http://localhost:3000 ...
start "RAG Frontend (Next.js)" cmd /k "cd frontend && npm run dev -- -H 0.0.0.0"

echo.
echo Waiting 5 seconds for servers to initialize...
timeout /t 5 /nobreak >nul

echo Opening browser at http://localhost:3000 ...
start http://localhost:3000

echo.
echo ======================================================================
echo Servers are running!
echo   - Local Web UI:    http://localhost:3000
echo   - Backend API:     http://localhost:8000/docs
echo   - Local Wi-Fi:     http://192.168.1.9:3000
echo ======================================================================
echo Keep the backend and frontend terminal windows open while using.
pause

