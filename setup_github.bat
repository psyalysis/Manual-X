@echo off
echo Setting up GitHub repository for Handskate...

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed or not in PATH. Please install Git first.
    pause
    exit /b 1
)

REM Initialize git repository
echo Initializing Git repository...
git init

REM Add remote origin (you'll need to replace with your actual GitHub repo URL)
echo.
echo IMPORTANT: You need to create a GitHub repository first!
echo Go to https://github.com/new and create a new repository named "Handskate"
echo Then replace the URL below with your actual repository URL.
echo.
set /p repo_url="Enter your GitHub repository URL (e.g., https://github.com/username/Handskate.git): "

if "%repo_url%"=="" (
    echo No URL provided. Exiting.
    pause
    exit /b 1
)

REM Add remote origin
echo Adding remote origin...
git remote add origin %repo_url%

REM Set default branch to main
echo Setting default branch to main...
git branch -M main

REM Add all files
echo Adding all files...
git add .

REM Initial commit
echo Making initial commit...
git commit -m "Initial commit - Handskate skateboard game"

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo Successfully set up GitHub repository!
    echo You can now use push_to_github.bat for future updates.
) else (
    echo.
    echo Failed to push to GitHub. Please check:
    echo 1. Your GitHub repository URL is correct
    echo 2. You have the correct permissions
    echo 3. Your GitHub credentials are set up
)

pause
