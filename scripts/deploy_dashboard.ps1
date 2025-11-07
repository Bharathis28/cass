# CASS-Lite v2 Dashboard - Cloud Run Deployment Script
# PowerShell script for Windows deployment

# Configuration
$PROJECT_ID = "cass-lite"
$REGION = "asia-south1"
$SERVICE_NAME = "cass-lite-dashboard"
$IMAGE_NAME = "gcr.io/$PROJECT_ID/dashboard"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "CASS-Lite v2 Dashboard - Cloud Run Deployment" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Set the active GCP project
Write-Host "[1/5] Setting GCP project to: $PROJECT_ID" -ForegroundColor Yellow
gcloud config set project $PROJECT_ID

# Step 2: Enable required APIs
Write-Host ""
Write-Host "[2/5] Enabling Cloud Run and Container Registry APIs..." -ForegroundColor Yellow
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Step 3: Build the Docker image
Write-Host ""
Write-Host "[3/5] Building Docker image..." -ForegroundColor Yellow
Write-Host "This may take 2-3 minutes..." -ForegroundColor Gray
docker build -t $IMAGE_NAME ./dashboard

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker image built successfully!" -ForegroundColor Green

# Step 4: Push to Google Container Registry
Write-Host ""
Write-Host "[4/5] Pushing image to GCR..." -ForegroundColor Yellow
docker push $IMAGE_NAME

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker push failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Image pushed to GCR!" -ForegroundColor Green

# Step 5: Deploy to Cloud Run
Write-Host ""
Write-Host "[5/5] Deploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy $SERVICE_NAME `
    --image=$IMAGE_NAME `
    --region=$REGION `
    --platform=managed `
    --allow-unauthenticated `
    --memory=512Mi `
    --cpu=1 `
    --timeout=300 `
    --max-instances=10 `
    --set-env-vars="GCP_PROJECT=cass-lite"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Cloud Run deployment failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "✅ DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your dashboard is now live at:" -ForegroundColor Cyan
Write-Host "https://$SERVICE_NAME-<random-id>.$REGION.run.app" -ForegroundColor White
Write-Host ""
Write-Host "To get the exact URL, run:" -ForegroundColor Yellow
Write-Host "gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)'" -ForegroundColor White
Write-Host ""
