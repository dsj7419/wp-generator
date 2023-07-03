@echo off
echo Checking for required Python packages...
python -m pip install numpy Pillow pyinstaller
echo.

echo Creating standalone executable with PyInstaller...
pyinstaller --onefile main.py
echo.

pause