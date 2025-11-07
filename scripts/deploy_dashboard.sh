#!/bin/bash
# CASS-Lite v2 Dashboard - Cloud Run Deployment Script
# Bash script for Linux/Mac deployment

# Configuration
PROJECT_ID="cass-lite"
REGION="asia-south1"
SERVICE_NAME="cass-lite-dashboard"
IMAGE_NAME="gcr.io/$PROJECT_ID/dashboard"

echo "================================================"
echo "CASS-Lite v2 Dashboard - Cloud Run Deployment"
echo "================================================"
echo ""

# Step 1: Set the active GCP project
echo "[1/5] Setting GCP project to: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Step 2: Enable required APIs
echo ""
echo "[2/5] Enabling Cloud Run and Container Registry APIs..."
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Step 3: Build the Docker image
echo ""
echo "[3/5] Building Docker image..."
echo "This may take 2-3 minutes..."
docker build -t $IMAGE_NAME ./dashboard

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed!"
    exit 1
fi

echo "✅ Docker image built successfully!"

# Step 4: Push to Google Container Registry
echo ""
echo "[4/5] Pushing image to GCR..."
docker push $IMAGE_NAME

if [ $? -ne 0 ]; then
    echo "❌ Docker push failed!"
    exit 1
fi

echo "✅ Image pushed to GCR!"

# Step 5: Deploy to Cloud Run
echo ""
echo "[5/5] Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image=$IMAGE_NAME \
    --region=$REGION \
    --platform=managed \
    --allow-unauthenticated \
    --memory=512Mi \
    --cpu=1 \
    --timeout=300 \
    --max-instances=10 \
    --set-env-vars="GCP_PROJECT=cass-lite"

if [ $? -ne 0 ]; then
    echo "❌ Cloud Run deployment failed!"
    exit 1
fi

echo ""
echo "================================================"
echo "✅ DEPLOYMENT SUCCESSFUL!"
echo "================================================"
echo ""
echo "Your dashboard is now live at:"
echo "https://$SERVICE_NAME-<random-id>.$REGION.run.app"
echo ""
echo "To get the exact URL, run:"
echo "gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)'"
echo ""
