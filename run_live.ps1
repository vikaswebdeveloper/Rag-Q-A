# PowerShell launcher for RAG Q&A Library
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "         LAUNCHING RAG Q&A DIGITAL LIBRARY (LIVE SYSTEM)              " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

$ProjectRoot = $PSScriptRoot

Write-Host "[1/2] Launching Backend on http://127.0.0.1:8000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ProjectRoot\backend'; ..\.venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8000 --reload"

Write-Host "[2/2] Launching Frontend on http://localhost:3000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ProjectRoot\frontend'; npm run dev -- -H 0.0.0.0"

Start-Sleep -Seconds 4

Write-Host ""
Write-Host "Opening web browser at http://localhost:3000 ..." -ForegroundColor Yellow
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "All servers are live!" -ForegroundColor Green
Write-Host "  • Desktop URL:    http://localhost:3000" -ForegroundColor White
Write-Host "  • Swagger API:    http://localhost:8000/docs" -ForegroundColor White
Write-Host "  • Local Wi-Fi:    http://192.168.1.9:3000" -ForegroundColor White
Write-Host "======================================================================" -ForegroundColor Cyan

