@echo off
for /f "delims=" %%i in (SILICONFLOW_API_KEY.txt) do set "SILICONFLOW_API_KEY=%%i"

:loop
echo [%time%] drawing...
python ".\draw_local.py"
echo [%time%] draw end, run task 1 hour later. 
timeout /t 3600 /nobreak >nul
goto loop