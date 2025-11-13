# 🚀 One-Click Cloud Deployment Guide

This guide explains how to deploy CASS-Lite v2 to Google Cloud using GitHub Actions with a single tag push.

---

## Prerequisites

1. **Google Cloud Project**
   - Project ID: `cass-lite` (or your custom project ID)
   - Billing enabled
   - Required APIs enabled (see below)

2. **GitHub Repository**
   - Repository with CASS-Lite v2 code
   - Admin access to configure secrets

3. **Local Tools** (for initial setup)
   - `gcloud` CLI installed and authenticated
   - Git configured

---

## Setup Steps

### Step 1: Enable Required Google Cloud APIs

```bash
# Authenticate to Google Cloud
gcloud auth login

# Set your project
gcloud config set project cass-lite

# Enable required APIs
gcloud services enable \
  cloudfunctions.googleapis.com \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  firestore.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com
```

### Step 2: Create Service Account for GitHub Actions

```bash
# Create service account
gcloud iam service-accounts create github-actions-deployer \
  --display-name="GitHub Actions Deployer for CASS-Lite"

# Grant necessary roles
gcloud projects add-iam-policy-binding cass-lite \
  --member="serviceAccount:github-actions-deployer@cass-lite.iam.gserviceaccount.com" \
  --role="roles/cloudfunctions.admin"

gcloud projects add-iam-policy-binding cass-lite \
  --member="serviceAccount:github-actions-deployer@cass-lite.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding cass-lite \
  --member="serviceAccount:github-actions-deployer@cass-lite.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding cass-lite \
  --member="serviceAccount:github-actions-deployer@cass-lite.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding cass-lite \
  --member="serviceAccount:github-actions-deployer@cass-lite.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

# Generate and download key
gcloud iam service-accounts keys create ~/gcp-key.json \
  --iam-account=github-actions-deployer@cass-lite.iam.gserviceaccount.com

# Display the key (you'll copy this to GitHub)
cat ~/gcp-key.json | base64
```

**Important:** Save the base64-encoded key. You'll need it in the next step.

### Step 3: Configure GitHub Repository Secret

1. Go to your GitHub repository
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `GCP_SA_KEY`
5. Value: Paste the entire JSON key from Step 2 (NOT base64 encoded, just the raw JSON)
6. Click **Add secret**

### Step 4: Update Project Configuration (if needed)

If your project ID is different from `cass-lite`, update the workflow file:

```yaml
# .github/workflows/deploy_on_tag.yaml
env:
  PROJECT_ID: your-project-id  # Change this
  REGION: asia-south1          # Change if needed
  PYTHON_VERSION: '3.11'
```

---

## Deployment

### Deploy via Git Tag

```bash
# Commit all changes
git add .
git commit -m "feat: Ready for deployment"
git push origin main

# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0
```

### Watch the Deployment

1. Go to GitHub repository → **Actions** tab
2. Click on the "Deploy to Google Cloud on Tag" workflow
3. Monitor the progress in real-time
4. Once complete, view the **Summary** tab for deployment URLs

---

## Deployment Output

After successful deployment, you'll get:

### 📦 Deployed Services

| Service | URL Pattern | Purpose |
|---------|-------------|---------|
| **Scheduler Function** | `https://<region>-<project>.cloudfunctions.net/cass-scheduler` | Makes carbon-aware scheduling decisions |
| **Worker Function** | `https://<region>-<project>.cloudfunctions.net/cass-worker` | Executes scheduled jobs |
| **Dashboard** | `https://cass-lite-dashboard-<hash>.<region>.run.app` | Interactive web dashboard |

### Example URLs (asia-south1, project: cass-lite)

```
Scheduler: https://asia-south1-cass-lite.cloudfunctions.net/cass-scheduler
Worker:    https://asia-south1-cass-lite.cloudfunctions.net/cass-worker
Dashboard: https://cass-lite-dashboard-262153469989.asia-south1.run.app
```

---

## Testing Your Deployment

### Test the Scheduler Function

```bash
# Test with POST request
curl -X POST "https://asia-south1-cass-lite.cloudfunctions.net/cass-scheduler" \
  -H "Content-Type: application/json" \
  -d '{"test": true}'

# Expected response:
# {
#   "success": true,
#   "status": "completed",
#   "decision": {
#     "region": "FI",
#     "carbon_intensity": 45,
#     "savings_gco2": 220
#   }
# }
```

### Test the Worker Function

```bash
curl -X POST "https://asia-south1-cass-lite.cloudfunctions.net/cass-worker" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "test-123",
    "region": "FI",
    "carbon_intensity": 45,
    "scheduled_at": "2025-11-13T10:00:00Z"
  }'
```

### Access the Dashboard

Simply open the dashboard URL in your browser:
```
https://cass-lite-dashboard-262153469989.asia-south1.run.app
```

---

## Monitoring

### View Logs

```bash
# Scheduler Function logs
gcloud functions logs read cass-scheduler \
  --gen2 \
  --region=asia-south1 \
  --limit=50

# Worker Function logs
gcloud functions logs read cass-worker \
  --gen2 \
  --region=asia-south1 \
  --limit=50

# Dashboard logs
gcloud run services logs read cass-lite-dashboard \
  --region=asia-south1 \
  --limit=50
```

### View in Console

- **Functions:** https://console.cloud.google.com/functions/list?project=cass-lite
- **Cloud Run:** https://console.cloud.google.com/run?project=cass-lite
- **Logs Explorer:** https://console.cloud.google.com/logs/query?project=cass-lite
- **Firestore:** https://console.cloud.google.com/firestore?project=cass-lite

---

## Updating the Deployment

To deploy a new version:

```bash
# Make your changes
git add .
git commit -m "feat: New feature"
git push origin main

# Create a new version tag
git tag v1.0.1
git push origin v1.0.1
```

The deployment workflow will automatically:
1. Build updated services
2. Deploy to Cloud Functions and Cloud Run
3. Post the new URLs to the GitHub Actions summary

---

## Rollback

If you need to rollback to a previous version:

```bash
# List all tags
git tag -l

# Checkout previous version
git checkout v1.0.0

# Create rollback tag
git tag v1.0.0-rollback
git push origin v1.0.0-rollback
```

Or rollback via Google Cloud Console:
1. Go to Cloud Functions or Cloud Run service
2. Click on **Revisions** tab
3. Select previous revision
4. Click **Manage Traffic** → Route 100% to previous revision

---

## Troubleshooting

### Deployment Failed

**Check the GitHub Actions logs:**
- Repository → Actions → Failed workflow run → View logs

**Common Issues:**

1. **Authentication Error**
   ```
   ERROR: (gcloud.auth.activate-service-account) Could not read json file
   ```
   **Fix:** Verify `GCP_SA_KEY` secret is set correctly (raw JSON, not base64)

2. **Permission Denied**
   ```
   ERROR: (gcloud.functions.deploy) PERMISSION_DENIED
   ```
   **Fix:** Ensure service account has all required roles (see Step 2)

3. **API Not Enabled**
   ```
   ERROR: API [cloudfunctions.googleapis.com] not enabled
   ```
   **Fix:** Run the API enable commands from Step 1

4. **Quota Exceeded**
   ```
   ERROR: Quota exceeded
   ```
   **Fix:** Check quotas in [GCP Console](https://console.cloud.google.com/iam-admin/quotas)

### Delete and Redeploy

If you need to start fresh:

```bash
# Delete all services
gcloud functions delete cass-scheduler --gen2 --region=asia-south1 --quiet
gcloud functions delete cass-worker --gen2 --region=asia-south1 --quiet
gcloud run services delete cass-lite-dashboard --region=asia-south1 --quiet

# Then push a new tag to redeploy
git tag v1.0.0-fresh
git push origin v1.0.0-fresh
```

---

## Cost Estimation

| Service | Pricing | Estimated Monthly Cost |
|---------|---------|------------------------|
| Cloud Functions (Scheduler) | $0.40/million invocations + compute | $1-5 |
| Cloud Functions (Worker) | $0.40/million invocations + compute | $1-5 |
| Cloud Run (Dashboard) | $0.00002400/vCPU-second + requests | $0.50-2 |
| Firestore | $0.06/100k reads, $0.18/100k writes | $0.50-3 |
| Cloud Build | First 120 builds/day free | $0 (within free tier) |
| **Total** | | **~$3-15/month** |

**Free Tier:**
- Cloud Functions: 2 million invocations/month free
- Cloud Run: 180,000 vCPU-seconds/month free
- Firestore: 50k reads, 20k writes/day free

---

## Security Considerations

1. **Service Account Key Rotation**
   ```bash
   # Rotate keys every 90 days
   gcloud iam service-accounts keys create ~/gcp-key-new.json \
     --iam-account=github-actions-deployer@cass-lite.iam.gserviceaccount.com
   
   # Update GitHub secret with new key
   # Delete old key
   gcloud iam service-accounts keys delete <OLD_KEY_ID> \
     --iam-account=github-actions-deployer@cass-lite.iam.gserviceaccount.com
   ```

2. **Enable Binary Authorization** (optional)
   ```bash
   gcloud services enable binaryauthorization.googleapis.com
   ```

3. **Use Secret Manager for API Keys** (recommended)
   ```bash
   # Store API key in Secret Manager
   echo -n "gwASf8vJiQ92CPIuRzuy" | \
     gcloud secrets create electricitymap-api-key --data-file=-
   
   # Grant access to Cloud Functions
   gcloud secrets add-iam-policy-binding electricitymap-api-key \
     --member="serviceAccount:github-actions-deployer@cass-lite.iam.gserviceaccount.com" \
     --role="roles/secretmanager.secretAccessor"
   ```

---

## Next Steps

After deployment:

1. ✅ Test all endpoints
2. ✅ Monitor logs for errors
3. ✅ Set up alerts in Cloud Monitoring
4. ✅ Configure custom domain (optional)
5. ✅ Enable Cloud Armor for DDoS protection (optional)
6. ✅ Set up Firestore backups

---

## Support

- **Documentation:** [README.md](../README.md)
- **Issues:** [GitHub Issues](https://github.com/Bharathis28/cass/issues)
- **Google Cloud Support:** https://cloud.google.com/support
