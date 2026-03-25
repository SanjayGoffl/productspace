@echo off
REM Load environment variables from .env file and run test

echo Loading environment variables from .env...

REM Read the .env file and set environment variables
for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
    set "line=%%a"
    if not "!line:~0,1!"=="#" (
        if not "%%a"=="" (
            set "%%a=%%b"
            echo Set %%a
        )
    )
)

echo.
echo Running test_market_setup.py...
echo.

python test_market_setup.py

pause
