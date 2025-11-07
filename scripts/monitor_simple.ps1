# ============================================================================
# CASS-Lite v2 - Cloud Monitoring Script (Simplified)
# ============================================================================

$PROJECT_ID = "cass-lite"
$REGION = "asia-south1"
$DASHBOARD_SERVICE = "cass-lite-dashboard"

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "CASS-Lite v2 - Monitoring Dashboard" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Project: $PROJECT_ID" -ForegroundColor White
Write-Host "Region: $REGION" -ForegroundColor White
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "Timestamp: $timestamp" -ForegroundColor White
Write-Host ""

# ============================================================================
# Service Status
# ============================================================================
Write-Host "SERVICE STATUS" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Gray

Write-Host ""
Write-Host "[Cloud Run] $DASHBOARD_SERVICE" -ForegroundColor Cyan
gcloud run services describe $DASHBOARD_SERVICE `
    --region=$REGION `
    --project=$PROJECT_ID `
    --format="value(status.url,status.conditions[0].status)" 2>&1

Write-Host ""
Write-Host "[Cloud Functions]" -ForegroundColor Cyan
$functions = @("run_scheduler", "run_worker_job")
foreach ($func in $functions) {
    $status = gcloud functions describe $func --region=$REGION --project=$PROJECT_ID --format="value(state)" 2>&1
    Write-Host "  $func : $status"
}

# ============================================================================
# Recent Logs
# ============================================================================
Write-Host ""
Write-Host "RECENT LOGS (Last 10)" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Gray

Write-Host ""
Write-Host "[Dashboard Logs]" -ForegroundColor Cyan
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=$DASHBOARD_SERVICE" `
    --limit=10 `
    --format="table(timestamp,severity)" `
    --project=$PROJECT_ID

# ============================================================================
# Error Check
# ============================================================================
Write-Host ""
Write-Host "ERROR CHECK (Last 24 hours)" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Gray

$errors = gcloud logging read "severity>=ERROR AND resource.type=cloud_run_revision AND resource.labels.service_name=$DASHBOARD_SERVICE" `
    --limit=5 `
    --format="value(timestamp)" `
    --project=$PROJECT_ID `
    --freshness=24h 2>&1

if ($errors -match "Listed 0 items" -or $errors.Count -eq 0) {
    Write-Host "[OK] No errors in the last 24 hours!" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Found errors:" -ForegroundColor Red
    Write-Host $errors
}

# ============================================================================
# Quick Links
# ============================================================================
Write-Host ""
Write-Host "QUICK LINKS" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Gray
Write-Host ""
Write-Host "Dashboard URL:" -ForegroundColor White
$url = gcloud run services describe $DASHBOARD_SERVICE --region=$REGION --project=$PROJECT_ID --format="value(status.url)" 2>&1
Write-Host "  $url" -ForegroundColor Cyan
Write-Host ""
Write-Host "Cloud Console:" -ForegroundColor White
Write-Host "  https://console.cloud.google.com/run/detail/$REGION/$DASHBOARD_SERVICE?project=$PROJECT_ID" -ForegroundColor Cyan
Write-Host ""
Write-Host "Logs Console:" -ForegroundColor White
Write-Host "  https://console.cloud.google.com/logs/query?project=$PROJECT_ID" -ForegroundColor Cyan
Write-Host ""

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "Monitoring check complete!" -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
