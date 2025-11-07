# CASS-Lite v2 Dashboard - Cloud Run Deployment Guide

## 📦 Files Created

Your dashboard is now containerized with the following files:

```
dashboard/
├── Dockerfile                    # Container configuration
├── .dockerignore                 # Excluded files from container
├── .streamlit/
│   └── config.toml              # Streamlit settings for Cloud Run
├── requirements.txt             # Dashboard-specific dependencies
├── app.py                       # Main dashboard application
└── utils.py                     # Data utilities
```

## 🚀 Quick Deployment (Automated)

### Option 1: PowerShell Script (Windows)
```powershell
cd "c:\Users\Admin\New folder\cass"
.\scripts\deploy_dashboard.ps1
```

### Option 2: Bash Script (Linux/Mac)
```bash
cd /path/to/cass
chmod +x scripts/deploy_dashboard.sh
./scripts/deploy_dashboard.sh
```

---

## 🔧 Manual Deployment (Step-by-Step)

If you prefer manual control, follow these commands:

### Prerequisites
```powershell
# Authenticate with Google Cloud
gcloud auth login

# Configure Docker for GCR
gcloud auth configure-docker

# Set active project
gcloud config set project cass-lite
```

### Step 1: Build the Docker Image
```powershell
cd "c:\Users\Admin\New folder\cass"

docker build -t gcr.io/cass-lite/dashboard ./dashboard
```

**Expected output:**
```
[+] Building 45.2s (10/10) FINISHED
=> [internal] load build definition from Dockerfile
=> => transferring dockerfile: 1.23kB
=> [internal] load .dockerignore
=> CACHED [1/5] FROM docker.io/library/python:3.11-slim
=> [2/5] WORKDIR /app
=> [3/5] COPY ../requirements.txt .
=> [4/5] RUN pip install --no-cache-dir -r requirements.txt
=> [5/5] COPY . .
=> exporting to image
=> => naming to gcr.io/cass-lite/dashboard
```

### Step 2: Push to Google Container Registry
```powershell
docker push gcr.io/cass-lite/dashboard
```

**Expected output:**
```
The push refers to repository [gcr.io/cass-lite/dashboard]
a1b2c3d4e5f6: Pushed
...
latest: digest: sha256:abc123... size: 3456
```

### Step 3: Deploy to Cloud Run
```powershell
gcloud run deploy cass-lite-dashboard `
    --image=gcr.io/cass-lite/dashboard `
    --region=asia-south1 `
    --platform=managed `
    --allow-unauthenticated `
    --memory=512Mi `
    --cpu=1 `
    --timeout=300 `
    --max-instances=10 `
    --set-env-vars="GCP_PROJECT=cass-lite"
```

**Expected output:**
```
Deploying container to Cloud Run service [cass-lite-dashboard] in project [cass-lite] region [asia-south1]
✓ Deploying new service... Done.
  ✓ Creating Revision...
  ✓ Routing traffic...
  ✓ Setting IAM Policy...
Done.
Service [cass-lite-dashboard] revision [cass-lite-dashboard-00001-abc] has been deployed and is serving 100 percent of traffic.
Service URL: https://cass-lite-dashboard-xyz123abc.asia-south1.run.app
```

---

## 🌐 Access Your Dashboard

### Get the Live URL
```powershell
gcloud run services describe cass-lite-dashboard --region=asia-south1 --format='value(status.url)'
```

**Expected URL format:**
```
https://cass-lite-dashboard-<random-id>.asia-south1.run.app
```

### Open in Browser
```powershell
# Windows PowerShell
Start-Process "https://cass-lite-dashboard-<your-id>.asia-south1.run.app"

# Or simply copy the URL and paste in your browser
```

---

## ✅ Verification Checklist

After deployment, verify these features:

- [ ] Dashboard loads with futuristic neon theme
- [ ] Hero section displays "CASS-Lite v2 Carbon Intelligence Dashboard"
- [ ] 4 metric cards show uniform size and white titles
- [ ] 3 interactive Plotly charts render correctly
- [ ] Live logs table displays mock data (or Firestore data if configured)
- [ ] Charts have white titles and bold labels
- [ ] Neon glow effects visible on hover
- [ ] Page is responsive and fast

---

## 🔐 Firestore Connection (Optional)

To connect to real Firestore data instead of mock data:

### 1. Create Service Account Key
```powershell
gcloud iam service-accounts create dashboard-sa --display-name="CASS Dashboard Service Account"

gcloud projects add-iam-policy-binding cass-lite `
    --member="serviceAccount:dashboard-sa@cass-lite.iam.gserviceaccount.com" `
    --role="roles/datastore.user"

gcloud iam service-accounts keys create dashboard-key.json `
    --iam-account=dashboard-sa@cass-lite.iam.gserviceaccount.com
```

### 2. Update Cloud Run with Credentials
```powershell
# Upload the key as a secret (recommended)
gcloud secrets create firestore-key --data-file=dashboard-key.json

# Update Cloud Run deployment
gcloud run services update cass-lite-dashboard `
    --region=asia-south1 `
    --update-secrets=GOOGLE_APPLICATION_CREDENTIALS=/secrets/firestore-key:latest
```

**Note:** On Cloud Run, Firestore should work automatically with Application Default Credentials (ADC) if the service account has proper permissions. The mock data fallback ensures the dashboard works regardless.

---

## 📊 Monitoring & Logs

### View Cloud Run Logs
```powershell
gcloud run services logs read cass-lite-dashboard --region=asia-south1 --limit=50
```

### Monitor Performance
```powershell
# Open Cloud Run console
Start-Process "https://console.cloud.google.com/run/detail/asia-south1/cass-lite-dashboard/metrics?project=cass-lite"
```

---

## 🛠️ Troubleshooting

### Issue: Docker build fails with "cannot find requirements.txt"
**Solution:** The Dockerfile copies from parent directory. Ensure you're in the project root:
```powershell
cd "c:\Users\Admin\New folder\cass"
docker build -t gcr.io/cass-lite/dashboard ./dashboard
```

### Issue: "Permission denied" when pushing to GCR
**Solution:** Configure Docker authentication:
```powershell
gcloud auth configure-docker
```

### Issue: Dashboard shows blank page
**Solution:** Check Cloud Run logs for errors:
```powershell
gcloud run services logs read cass-lite-dashboard --region=asia-south1 --limit=100
```

### Issue: Firestore connection warnings
**Solution:** This is expected when running locally. On Cloud Run, it will use Application Default Credentials automatically. Alternatively, configure service account credentials as shown above.

---

## 🔄 Update Deployment

To update the dashboard after code changes:

```powershell
# Rebuild the image
docker build -t gcr.io/cass-lite/dashboard ./dashboard

# Push updated image
docker push gcr.io/cass-lite/dashboard

# Cloud Run will automatically deploy the new version
# Or force redeployment:
gcloud run services update cass-lite-dashboard --region=asia-south1
```

---

## 💰 Cost Estimate

**Cloud Run Pricing (asia-south1):**
- First 2 million requests/month: FREE
- CPU: $0.00002400 per vCPU-second
- Memory: $0.00000250 per GiB-second
- Requests: $0.40 per million requests

**Estimated monthly cost for low traffic (~1000 requests/month):**
- **FREE** (within free tier limits)

**For medium traffic (~100k requests/month):**
- Approximately **$5-10/month**

---

## 📋 Summary

✅ **Dockerfile Created**: Python 3.11 base, optimized for Cloud Run
✅ **Streamlit Config**: Port 8080, headless mode, CORS disabled
✅ **Dependencies**: Minimal requirements.txt for fast builds
✅ **Deployment Scripts**: Automated PowerShell and Bash scripts
✅ **Folder Structure**: Preserved exactly as required
✅ **No Code Changes**: app.py and utils.py remain untouched

**Your dashboard is ready to deploy!** 🚀

Run the deployment script or follow the manual steps above to go live on Cloud Run.
