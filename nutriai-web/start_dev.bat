@echo off
title NutriAI Full-Stack Development Server
echo =========================================================
echo   Starting NutriAI Web Full-Stack Platform (Local Dev)
echo =========================================================

echo [1/2] Launching Python FastAPI Backend on http://127.0.0.1:8000 ...
start "NutriAI Backend (FastAPI)" cmd /k "cd /d %~dp0backend && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Launching Next.js Frontend on http://localhost:3000 ...
start "NutriAI Frontend (Next.js)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo NutriAI processes started in separate windows!
echo - Frontend UI:      http://localhost:3000
echo - Backend API:      http://127.0.0.1:8000
echo - Swagger Docs:     http://127.0.0.1:8000/docs
echo - Demo Account:     demo@nutriai.com / Demo@1234
echo.
pause
