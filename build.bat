@echo off

echo Checking if Python is installed...
where python >nul 2>&1
if %errorlevel% neq 0 (
echo Python is not installed. Please install Python and ensure it is added to the system's PATH.
pause
exit /b 1
)
echo Python is installed.
echo.

echo Checking for required Python packages...
python -m pip install numpy Pillow pyinstaller
echo.

echo Checking for Microsoft Visual C++ Build Tools...
where cl >nul 2>&1
if %errorlevel% neq 0 (
echo Microsoft Visual C++ Build Tools not found. Please install it manually.
echo You can download it from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
pause
exit /b 1
)
echo Microsoft Visual C++ Build Tools found.
echo.

echo Checking for noise package...
python -c "import noise" >nul 2>&1
if %errorlevel% neq 0 (
echo Installing noise package...
python -m pip install noise
)
echo noise package found or installed.
echo.

echo Creating standalone executable with PyInstaller...
pyinstaller --onefile --add-data "gui;gui" --add-data "settings;settings" --add-data "generators;generators" --add-data "logger;logger" --hidden-import tkinter main.py
echo.

pause