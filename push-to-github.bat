@echo off
REM StadiumAI - Push to GitHub Script
cd /d d:\StadiumAI

echo ========================================
echo   StadiumAI - Pushing to GitHub
echo ========================================
echo.

echo [1/5] Configuring git...
git config --global user.name "StadiumAI Developer"
git config --global user.email "admin@stadiumai.example"

echo [2/5] Staging files...
git add .

echo [3/5] Creating commit...
git commit -m "Initial commit: StadiumAI - AI-powered smart stadium operations platform for FIFA World Cup 2026"

echo [4/5] Adding remote...
git remote add origin https://github.com/sainadhpuvvada2005-ui/StadiumAI.git

echo [5/5] Pushing to GitHub...
git branch -M main
git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ========================================
    echo   SUCCESS! Repository pushed!
    echo ========================================
    echo.
    echo Repository: https://github.com/sainadhpuvvada2005-ui/StadiumAI
    echo.
) else (
    echo.
    echo ERROR during push. Check your credentials.
    echo.
)

pause
