@echo off
echo Checking for required Python packages...
python -m pip install numpy Pillow pyinstaller
echo.

echo Creating standalone executable with PyInstaller...
pyinstaller --onefile --add-data "gui;gui" --add-data "settings;settings" --add-data "generators;generators" --add-data "logger;logger" --hidden-import tkinter main.py
echo.

pause
