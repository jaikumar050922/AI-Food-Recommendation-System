Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "  Starting NutriAI Web Full-Stack Platform (Local Dev)   " -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Start Python FastAPI Backend in background
Write-Host "`n[1/2] Launching Python FastAPI Backend on http://127.0.0.1:8000 ..." -ForegroundColor Green
$BackendProcess = Start-Process python -ArgumentList "-m uvicorn main:app --host 127.0.0.1 --port 8000 --reload" -WorkingDirectory "$ScriptDir\backend" -PassThru

# 2. Start Next.js Frontend
Write-Host "[2/2] Launching Next.js Frontend on http://localhost:3000 ..." -ForegroundColor Green
Start-Process npm -ArgumentList "run dev" -WorkingDirectory "$ScriptDir\frontend"

Write-Host "`nNutriAI is starting up!" -ForegroundColor Cyan
Write-Host "  - Frontend Portal:  http://localhost:3000" -ForegroundColor Yellow
Write-Host "  - Backend API:      http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host "  - API Swagger Docs: http://127.0.0.1:8000/docs" -ForegroundColor Yellow
Write-Host "  - Demo User:        demo@nutriai.com / Demo@1234`n" -ForegroundColor Yellow
