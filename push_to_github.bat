@echo off
echo ======================================================================
echo Pushing EdTech A/B Testing & Causal Analysis repository to GitHub...
echo Target: https://github.com/Priyansu17/EdTech-Experiment-Causal-Analysis
echo ======================================================================
git push -u origin main
if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUCCESS] Repository successfully pushed to GitHub!
    echo URL: https://github.com/Priyansu17/EdTech-Experiment-Causal-Analysis
) else (
    echo.
    echo [ACTION REQUIRED]:
    echo 1. Open your browser and go to: https://github.com/new
    echo 2. Set 'Repository name' to: EdTech-Experiment-Causal-Analysis
    echo 3. Leave it Public and click 'Create repository' (Do not add README or .gitignore)
    echo 4. Run this script again, and it will push instantly with your saved credentials!
)
pause
