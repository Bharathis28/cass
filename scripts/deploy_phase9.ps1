# ============================================================================
# CASS-Lite v2 - Phase 9 Deployment Script
# ============================================================================
# Purpose: Deploy enhanced dashboard with Phase 9 features to Cloud Run
# Author: Bharathi Senthilkumar
# Date: November 2025
# ============================================================================

Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host " CASS-Lite v2 - Phase 9 Deployment " -NoNewline -ForegroundColor White
Write-Host "=" -ForegroundColor Cyan
Write-Host ""

$PROJECT_ID = "cass-lite"
$REGION = "asia-south1"
$SERVICE_NAME = "cass-lite-dashboard"
$IMAGE_TAG = "phase9"
$IMAGE_NAME = "gcr.io/$PROJECT_ID/$SERVICE_NAME`:$IMAGE_TAG"

# ============================================================================
# STEP 1: Verify Prerequisites
# ============================================================================

Write-Host "[1/6] Verifying prerequisites..." -ForegroundColor Yellow

# Check if gcloud is installed
try {
    $gcloudVersion = gcloud version --format="value(core.version)" 2>$null
    Write-Host "  gcloud CLI: v$gcloudVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: gcloud CLI not found. Please install Google Cloud SDK." -ForegroundColor Red
    exit 1
}

# Check if Docker is running
try {
    docker info 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Docker: Running" -ForegroundColor Green
    } else {
        throw "Docker not running"
    }
} catch {
    Write-Host "  WARNING: Docker not running. Starting Docker Desktop..." -ForegroundColor Yellow
    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    Write-Host "  Waiting for Docker to start (30 seconds)..."
    Start-Sleep -Seconds 30
}

# Check if authenticated to GCP
try {
    $currentProject = gcloud config get-value project 2>$null
    if ($currentProject -eq $PROJECT_ID) {
        Write-Host "  GCP Project: $currentProject" -ForegroundColor Green
    } else {
        Write-Host "  Setting project to $PROJECT_ID..." -ForegroundColor Yellow
        gcloud config set project $PROJECT_ID
    }
} catch {
    Write-Host "  ERROR: Not authenticated to GCP. Run: gcloud auth login" -ForegroundColor Red
    exit 1
}

Write-Host ""

# ============================================================================
# STEP 2: Build Docker Image
# ============================================================================

Write-Host "[2/6] Building Docker image..." -ForegroundColor Yellow

$buildStart = Get-Date

# Change to project root
Set-Location "c:\Users\Admin\New folder\cass"

# Build image
Write-Host "  Building: $IMAGE_NAME" -ForegroundColor Cyan
docker build -t $IMAGE_NAME -f dashboard/Dockerfile . 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    $buildDuration = (Get-Date) - $buildStart
    Write-Host "  Build successful ($([math]::Round($buildDuration.TotalSeconds, 1))s)" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Docker build failed" -ForegroundColor Red
    exit 1
}

# Get image size
$imageSize = docker images $IMAGE_NAME --format "{{.Size}}"
Write-Host "  Image size: $imageSize" -ForegroundColor Green

Write-Host ""

# ============================================================================
# STEP 3: Configure Docker Authentication
# ============================================================================

Write-Host "[3/6] Configuring Docker authentication..." -ForegroundColor Yellow

try {
    gcloud auth configure-docker gcr.io --quiet 2>&1 | Out-Null
    Write-Host "  Docker authentication configured" -ForegroundColor Green
} catch {
    Write-Host "  WARNING: Authentication may already be configured" -ForegroundColor Yellow
}

Write-Host ""

# ============================================================================
# STEP 4: Push Image to GCR
# ============================================================================

Write-Host "[4/6] Pushing image to Container Registry..." -ForegroundColor Yellow

$pushStart = Get-Date

docker push $IMAGE_NAME 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    $pushDuration = (Get-Date) - $pushStart
    Write-Host "  Push successful ($([math]::Round($pushDuration.TotalSeconds, 1))s)" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Docker push failed" -ForegroundColor Red
    exit 1
}

Write-Host ""

# ============================================================================
# STEP 5: Deploy to Cloud Run
# ============================================================================

Write-Host "[5/6] Deploying to Cloud Run..." -ForegroundColor Yellow

$deployStart = Get-Date

# Deploy service
gcloud run deploy $SERVICE_NAME `
    --image $IMAGE_NAME `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --memory 512Mi `
    --cpu 1 `
    --min-instances 0 `
    --max-instances 10 `
    --port 8501 `
    --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID" `
    --quiet 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    $deployDuration = (Get-Date) - $deployStart
    Write-Host "  Deployment successful ($([math]::Round($deployDuration.TotalSeconds, 1))s)" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Cloud Run deployment failed" -ForegroundColor Red
    exit 1
}

Write-Host ""

# ============================================================================
# STEP 6: Verify Deployment
# ============================================================================

Write-Host "[6/6] Verifying deployment..." -ForegroundColor Yellow

# Get service URL
$serviceUrl = gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)" 2>$null

if ($serviceUrl) {
    Write-Host "  Service URL: $serviceUrl" -ForegroundColor Green
    
    # Test endpoint
    try {
        $response = Invoke-WebRequest -Uri $serviceUrl -TimeoutSec 30 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "  Health check: PASSED" -ForegroundColor Green
        } else {
            Write-Host "  Health check: FAILED (HTTP $($response.StatusCode))" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  Health check: Service starting (may take 1-2 minutes)" -ForegroundColor Yellow
    }
} else {
    Write-Host "  WARNING: Could not retrieve service URL" -ForegroundColor Yellow
}

# Display service details
Write-Host ""
Write-Host "Service Details:" -ForegroundColor Cyan
Write-Host "  Name: $SERVICE_NAME" -ForegroundColor White
Write-Host "  Region: $REGION" -ForegroundColor White
Write-Host "  Image: $IMAGE_NAME" -ForegroundColor White
Write-Host "  Memory: 512 MB" -ForegroundColor White
Write-Host "  CPU: 1 vCPU" -ForegroundColor White
Write-Host "  Min Instances: 0" -ForegroundColor White
Write-Host "  Max Instances: 10" -ForegroundColor White

Write-Host ""

# ============================================================================
# DEPLOYMENT SUMMARY
# ============================================================================

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host " DEPLOYMENT COMPLETE " -NoNewline -ForegroundColor White
Write-Host "=" -ForegroundColor Cyan
Write-Host ""

Write-Host "Phase 9 Features Deployed:" -ForegroundColor Green
Write-Host "  Auto-refresh (30s)" -ForegroundColor White
Write-Host "  Geographic heatmap" -ForegroundColor White
Write-Host "  Energy mix chart" -ForegroundColor White
Write-Host "  AI insights (6 cards)" -ForegroundColor White
Write-Host "  CSV/JSON export" -ForegroundColor White
Write-Host "  Animated UI elements" -ForegroundColor White
Write-Host "  Cloud Run metrics" -ForegroundColor White
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Visit: $serviceUrl" -ForegroundColor White
Write-Host "  2. Verify all Phase 9 features working" -ForegroundColor White
Write-Host "  3. Test auto-refresh and exports" -ForegroundColor White
Write-Host "  4. Monitor logs: .\scripts\monitor_simple.ps1" -ForegroundColor White
Write-Host "  5. Check costs: .\scripts\cost_report.ps1" -ForegroundColor White
Write-Host ""

# Open dashboard in browser (optional)
$openBrowser = Read-Host "Open dashboard in browser? (Y/N)"
if ($openBrowser -eq "Y" -or $openBrowser -eq "y") {
    Start-Process $serviceUrl
}

Write-Host ""
Write-Host "Deployment completed successfully!" -ForegroundColor Green
Write-Host ""

# ============================================================================
# END OF SCRIPT
# ============================================================================
