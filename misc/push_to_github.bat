@echo off
echo Initializing Git repository and pushing to GitHub...

REM Initialize git repository if it doesn't exist
if not exist ".git" (
    echo Initializing Git repository...
    git init
)

REM Add all files to staging
echo Adding files to staging...
git add .

REM Check if there are any changes to commit
git diff --cached --quiet
if %errorlevel% equ 0 (
    echo No changes to commit.
    pause
    exit /b 0
)

REM Commit changes
echo Committing changes...
git commit -m "Update Handskate project"

REM Check if remote origin exists
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo Please set up GitHub remote first:
    echo git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    echo Then run this script again.
    pause
    exit /b 1
)

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo Successfully pushed to GitHub!
) else (
    echo Failed to push to GitHub. Check your remote URL and credentials.
)

pause
