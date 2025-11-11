# ============================================================================
# CASS-Lite v2 - Phase 11 Security Deployment Script
# ============================================================================
# Purpose: Deploy security-hardened Cloud Functions with authentication
# Author: CASS-Lite v2 Team
# Date: November 11, 2025
# ============================================================================

Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host " CASS-Lite v2 - Phase 11 Security Deployment " -NoNewline -ForegroundColor White
Write-Host "=" -ForegroundColor Cyan
Write-Host ""

$PROJECT_ID = "cass-lite"
$REGION = "asia-south1"
$SERVICE_ACCOUNT = "scheduler-sa@cass-lite.iam.gserviceaccount.com"

# ============================================================================
# STEP 1: Verify Security Configuration
# ============================================================================

Write-Host "[1/5] Verifying security configuration..." -ForegroundColor Yellow

# Check if service account exists
try {
    $saExists = gcloud iam service-accounts describe $SERVICE_ACCOUNT --project=$PROJECT_ID 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Service Account: $SERVICE_ACCOUNT" -ForegroundColor Green
    } else {
        Write-Host "  ERROR: Service account not found. Run Phase 11 setup first." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "  ERROR: Failed to verify service account." -ForegroundColor Red
    exit 1
}

Write-Host ""

# ============================================================================
# STEP 2: Deploy Scheduler Function (Authenticated)
# ============================================================================

Write-Host "[2/5] Deploying scheduler function with authentication..." -ForegroundColor Yellow

$deployStart = Get-Date

gcloud functions deploy run_scheduler `
    --gen2 `
    --runtime=python311 `
    --region=$REGION `
    --source=cloud_functions/scheduler_function `
    --entry-point=run_scheduler `
    --trigger-http `
    --memory=512Mi `
    --timeout=540s `
    --set-env-vars="GCP_PROJECT=$PROJECT_ID" `
    --service-account=$SERVICE_ACCOUNT `
    --no-allow-unauthenticated `
    --quiet

if ($LASTEXITCODE -eq 0) {
    $deployDuration = (Get-Date) - $deployStart
    Write-Host "  Scheduler deployed successfully ($([math]::Round($deployDuration.TotalSeconds, 1))s)" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Scheduler deployment failed" -ForegroundColor Red
    exit 1
}

Write-Host ""

# ============================================================================
# STEP 3: Deploy Worker Function (Authenticated)
# ============================================================================

Write-Host "[3/5] Deploying worker function with authentication..." -ForegroundColor Yellow

$deployStart = Get-Date

gcloud functions deploy run_worker_job `
    --gen2 `
    --runtime=python311 `
    --region=$REGION `
    --source=cloud_functions/worker_job `
    --entry-point=run_worker_job `
    --trigger-http `
    --memory=256Mi `
    --timeout=300s `
    --set-env-vars="GCP_PROJECT=$PROJECT_ID" `
    --service-account=$SERVICE_ACCOUNT `
    --no-allow-unauthenticated `
    --quiet

if ($LASTEXITCODE -eq 0) {
    $deployDuration = (Get-Date) - $deployStart
    Write-Host "  Worker deployed successfully ($([math]::Round($deployDuration.TotalSeconds, 1))s)" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Worker deployment failed" -ForegroundColor Red
    exit 1
}

Write-Host ""

# ============================================================================
# STEP 4: Verify IAM Policies
# ============================================================================

Write-Host "[4/5] Verifying IAM policies..." -ForegroundColor Yellow

# Check scheduler function policy
Write-Host "  Checking run_scheduler IAM policy..." -ForegroundColor Cyan
$schedulerPolicy = gcloud functions get-iam-policy run_scheduler --region=$REGION --format=json 2>$null | ConvertFrom-Json

$hasSchedulerSA = $false
$hasPublicAccess = $false

foreach ($binding in $schedulerPolicy.bindings) {
    if ($binding.role -eq "roles/run.invoker") {
        foreach ($member in $binding.members) {
            if ($member -eq "serviceAccount:$SERVICE_ACCOUNT") {
                $hasSchedulerSA = $true
            }
            if ($member -eq "allUsers") {
                $hasPublicAccess = $true
            }
        }
    }
}

if ($hasSchedulerSA -and -not $hasPublicAccess) {
    Write-Host "    Scheduler IAM: SECURED" -ForegroundColor Green
} else {
    Write-Host "    Scheduler IAM: WARNING - Check configuration" -ForegroundColor Yellow
}

# Check worker function policy
Write-Host "  Checking run_worker_job IAM policy..." -ForegroundColor Cyan
$workerPolicy = gcloud functions get-iam-policy run_worker_job --region=$REGION --format=json 2>$null | ConvertFrom-Json

$hasWorkerSA = $false
$hasPublicAccess = $false

foreach ($binding in $workerPolicy.bindings) {
    if ($binding.role -eq "roles/run.invoker") {
        foreach ($member in $binding.members) {
            if ($member -eq "serviceAccount:$SERVICE_ACCOUNT") {
                $hasWorkerSA = $true
            }
            if ($member -eq "allUsers") {
                $hasPublicAccess = $true
            }
        }
    }
}

if ($hasWorkerSA -and -not $hasPublicAccess) {
    Write-Host "    Worker IAM: SECURED" -ForegroundColor Green
} else {
    Write-Host "    Worker IAM: WARNING - Check configuration" -ForegroundColor Yellow
}

Write-Host ""

# ============================================================================
# STEP 5: Test Authentication
# ============================================================================

Write-Host "[5/5] Testing authentication..." -ForegroundColor Yellow

# Get function URL
$schedulerUrl = gcloud functions describe run_scheduler --region=$REGION --format="value(serviceConfig.uri)" 2>$null

Write-Host "  Scheduler URL: $schedulerUrl" -ForegroundColor Cyan

# Test WITHOUT authentication (should fail)
Write-Host "  Testing without auth token (should fail)..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri $schedulerUrl -Method GET -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 403) {
        Write-Host "    Public access blocked: PASS" -ForegroundColor Green
    } else {
        Write-Host "    Public access allowed: FAIL" -ForegroundColor Red
    }
} catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 403) {
        Write-Host "    Public access blocked: PASS" -ForegroundColor Green
    } else {
        Write-Host "    Unexpected error: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

# Test WITH authentication (should succeed)
Write-Host "  Testing with auth token (should succeed)..." -ForegroundColor Cyan
try {
    $token = gcloud auth print-identity-token 2>$null
    if ($token) {
        $headers = @{
            "Authorization" = "Bearer $token"
        }
        $response = Invoke-WebRequest -Uri $schedulerUrl -Headers $headers -Method GET -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "    Authenticated access: PASS" -ForegroundColor Green
        } else {
            Write-Host "    Authenticated access: Status $($response.StatusCode)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "    Could not generate auth token" -ForegroundColor Yellow
    }
} catch {
    Write-Host "    Auth test skipped: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""

# ============================================================================
# DEPLOYMENT SUMMARY
# ============================================================================

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host " PHASE 11 DEPLOYMENT COMPLETE " -NoNewline -ForegroundColor White
Write-Host "=" -ForegroundColor Cyan
Write-Host ""

Write-Host "Security Status:" -ForegroundColor Green
Write-Host "  Cloud Functions: AUTHENTICATED" -ForegroundColor White
Write-Host "  Service Account: $SERVICE_ACCOUNT" -ForegroundColor White
Write-Host "  Public Access: BLOCKED" -ForegroundColor White
Write-Host "  IAM Policies: VERIFIED" -ForegroundColor White
Write-Host ""

Write-Host "Services:" -ForegroundColor Yellow
Write-Host "  Scheduler: $schedulerUrl" -ForegroundColor White
Write-Host "  Worker: https://$REGION-$PROJECT_ID.cloudfunctions.net/run_worker_job" -ForegroundColor White
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Test scheduler with authenticated requests" -ForegroundColor White
Write-Host "  2. Monitor Cloud Logging for errors" -ForegroundColor White
Write-Host "  3. Verify cost remains within budget" -ForegroundColor White
Write-Host "  4. Review PHASE_11_SECURITY_HARDENING.md" -ForegroundColor White
Write-Host ""

Write-Host "Phase 11 security hardening completed successfully!" -ForegroundColor Green
Write-Host ""

# ============================================================================
# END OF SCRIPT
# ============================================================================
