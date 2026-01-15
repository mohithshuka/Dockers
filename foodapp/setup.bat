@echo off
echo ========================================
echo Food Delivery App - Setup Script
echo ========================================

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo Creating directories...
if not exist "static\images" mkdir static\images

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Please add food images to static\images\ folder:
echo   - default.jpg (required)
echo   - pizza.jpg, burger.jpg, salad.jpg, etc. (optional)
echo.
echo To run the application:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run the app: python app.py
echo   3. Open browser: http://localhost:5000
echo.
echo Default admin credentials:
echo   Email: admin@food.com
echo   Password: admin123
echo.
pause