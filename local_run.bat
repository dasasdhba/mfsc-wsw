@echo off
for /f "delims=" %%i in (SILICONFLOW_API_KEY.txt) do set "SILICONFLOW_API_KEY=%%i"

echo [%time%] drawing...
python ".\draw_local.py"
pause