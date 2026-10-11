@echo off
echo Starting Juego 21 (Game 21)...
if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe main.py %*
) else (
    python main.py %*
)
pause
