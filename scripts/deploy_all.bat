@echo off
REM ========================================================================
REM CASS-Lite v2 - Cloud Run Functions Deployment Script (Windows)
REM ========================================================================

echo ========================================================================
echo  CASS-LITE v2 - Cloud Run Functions Deployment
echo ========================================================================
echo.

REM Check if gcloud is installed
where gcloud >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: gcloud CLI is not installed
    echo Download from: https://cloud.google.com/sdk/docs/install
    exit /b 1
)

echo [OK] gcloud CLI found
echo.

REM Get current project
for /f "tokens=*" %%i in ('gcloud config get-value project 2^>nul') do set PROJECT_ID=%%i
if "%PROJECT_ID%"=="" (
    echo WARNING: No GCP project configured
    echo Run: gcloud config set project YOUR_PROJECT_ID
    pause
    exit /b 1
)

echo [OK] Using GCP Project: %PROJECT_ID%
echo.

REM ========================================================================
echo ========================================================================
echo  Step 1: Deploying Worker Function
echo ========================================================================
echo.

cd /d "c:\Users\Admin\New folder\cass\cloud_functions\worker_job"

echo Deploying run_worker_job to asia-south1...
gcloud functions deploy run_worker_job ^
  --runtime=python311 ^
  --region=asia-south1 ^
  --source=. ^
  --entry-point=run_worker_job ^
  --trigger-http ^
  --allow-unauthenticated ^
  --memory=256Mi ^
  --timeout=300s

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Worker function deployment failed!
    pause
    exit /b 1
)

echo.
echo [OK] Worker function deployed successfully!
echo.

REM ========================================================================
echo ========================================================================
echo  Step 2: Deploying Scheduler Function
echo ========================================================================
echo.

cd /d "c:\Users\Admin\New folder\cass\cloud_functions\scheduler_function"

echo Deploying run_scheduler to asia-south1...
gcloud functions deploy run_scheduler ^
  --runtime=python311 ^
  --region=asia-south1 ^
  --source=. ^
  --entry-point=run_scheduler ^
  --trigger-http ^
  --allow-unauthenticated ^
  --memory=512Mi ^
  --timeout=540s

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Scheduler function deployment failed!
    pause
    exit /b 1
)

echo.
echo [OK] Scheduler function deployed successfully!
echo.

REM ========================================================================
echo ========================================================================
echo  Deployment Complete!
echo ========================================================================
echo.
echo Both functions have been deployed to Cloud Run Functions.
echo.
echo Next steps:
echo 1. Test the worker function with curl
echo 2. Test the scheduler function
echo 3. Update scheduler/config.json with function URLs
echo 4. Build the Streamlit dashboard
echo.
echo To view your functions:
echo   gcloud functions list
echo.
echo To view logs:
echo   gcloud functions logs read run_worker_job --region=asia-south1
echo   gcloud functions logs read run_scheduler --region=asia-south1
echo.
echo ========================================================================
echo.
pause
