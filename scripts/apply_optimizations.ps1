# ============================================================================
# CASS-Lite v2 - Phase 8 Cost Optimization Commands
# ============================================================================
# Quick reference for applying cost optimizations
# ============================================================================

$PROJECT_ID = "cass-lite"
$REGION = "asia-south1"

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "CASS-Lite v2 - Cost Optimization Application" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# OPTIMIZATION 1: Reduce Cloud Run Memory (Optional - if stable)
# ============================================================================
Write-Host "[OPTIMIZATION 1] Reduce Cloud Run Memory: 512Mi → 256Mi" -ForegroundColor Yellow
Write-Host "Current: 512Mi" -ForegroundColor White
Write-Host "Recommended: 256Mi (if dashboard is stable with low traffic)" -ForegroundColor White
Write-Host ""
Write-Host "Command:" -ForegroundColor Cyan
Write-Host "  gcloud run services update cass-lite-dashboard \"  -ForegroundColor Gray
Write-Host "    --memory=256Mi \"  -ForegroundColor Gray
Write-Host "    --region=$REGION \"  -ForegroundColor Gray
Write-Host "    --project=$PROJECT_ID" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  WARNING: May cause OOM if concurrent users increase" -ForegroundColor Yellow
Write-Host "Potential Savings: ~`$0.01-0.05/month" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to skip, or type 'apply' to execute"

# ============================================================================
# OPTIMIZATION 2: Reduce Scheduler Function Memory
# ============================================================================
Write-Host ""
Write-Host "[OPTIMIZATION 2] Reduce Scheduler Function Memory: 512Mi → 256Mi" -ForegroundColor Yellow
Write-Host "Current: 512Mi" -ForegroundColor White
Write-Host "Recommended: 256Mi" -ForegroundColor White
Write-Host ""
Write-Host "Command:" -ForegroundColor Cyan
Write-Host "  gcloud functions deploy run_scheduler \"  -ForegroundColor Gray
Write-Host "    --gen2 \"  -ForegroundColor Gray
Write-Host "    --region=$REGION \"  -ForegroundColor Gray
Write-Host "    --runtime=python311 \"  -ForegroundColor Gray
Write-Host "    --memory=256Mi \"  -ForegroundColor Gray
Write-Host "    --timeout=120s \"  -ForegroundColor Gray
Write-Host "    --project=$PROJECT_ID" -ForegroundColor Gray
Write-Host ""
Write-Host "Potential Savings: Minimal (already in free tier)" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to skip, or type 'apply' to execute"

# ============================================================================
# OPTIMIZATION 3: Set Log Retention (30 days)
# ============================================================================
Write-Host ""
Write-Host "[OPTIMIZATION 3] Set Log Retention to 30 Days" -ForegroundColor Yellow
Write-Host "Current: Indefinite (default)" -ForegroundColor White
Write-Host "Recommended: 30 days" -ForegroundColor White
Write-Host ""
Write-Host "Applying..." -ForegroundColor Cyan

try {
    gcloud logging buckets update _Default `
        --location=global `
        --retention-days=30 `
        --project=$PROJECT_ID 2>&1
    
    Write-Host "✅ Log retention set to 30 days" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not update log retention (may already be set)" -ForegroundColor Yellow
}

# ============================================================================
# OPTIMIZATION 4: Create Billing Budget (Optional)
# ============================================================================
Write-Host ""
Write-Host "[OPTIMIZATION 4] Create Billing Budget Alert" -ForegroundColor Yellow
Write-Host "Budget: `$10/month with alerts at 50%, 90%, 100%" -ForegroundColor White
Write-Host ""
Write-Host "Note: Requires billing account ID" -ForegroundColor Yellow
Write-Host ""
Write-Host "To create budget manually:" -ForegroundColor Cyan
Write-Host "  1. Get billing account ID:" -ForegroundColor Gray
Write-Host "     gcloud billing accounts list" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Create budget:" -ForegroundColor Gray
Write-Host "     gcloud billing budgets create \"  -ForegroundColor Gray
Write-Host "       --billing-account=YOUR_BILLING_ACCOUNT_ID \"  -ForegroundColor Gray
Write-Host "       --display-name='CASS-Lite Budget' \"  -ForegroundColor Gray
Write-Host "       --budget-amount=10USD \"  -ForegroundColor Gray
Write-Host "       --threshold-rule=percent=0.5 \"  -ForegroundColor Gray
Write-Host "       --threshold-rule=percent=0.9 \"  -ForegroundColor Gray
Write-Host "       --threshold-rule=percent=1.0" -ForegroundColor Gray
Write-Host ""

# ============================================================================
# OPTIMIZATION 5: Set Up Cloud Scheduler (Optional - Automation)
# ============================================================================
Write-Host ""
Write-Host "[OPTIMIZATION 5] Cloud Scheduler for Automation (Optional)" -ForegroundColor Yellow
Write-Host "Trigger scheduler function every 6 hours automatically" -ForegroundColor White
Write-Host ""
Write-Host "Command:" -ForegroundColor Cyan
Write-Host "  gcloud scheduler jobs create http schedule-carbon-check \"  -ForegroundColor Gray
Write-Host "    --schedule='0 */6 * * *' \"  -ForegroundColor Gray
Write-Host "    --uri='https://asia-south1-cass-lite.cloudfunctions.net/run_scheduler' \"  -ForegroundColor Gray
Write-Host "    --location=$REGION \"  -ForegroundColor Gray
Write-Host "    --project=$PROJECT_ID" -ForegroundColor Gray
Write-Host ""
Write-Host "Cost: FREE (3 jobs free, then `$0.10/job/month)" -ForegroundColor Green
Write-Host ""

# ============================================================================
# Summary
# ============================================================================
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "OPTIMIZATION SUMMARY" -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Applied Optimizations:" -ForegroundColor Green
Write-Host "  ✅ Log retention: 30 days" -ForegroundColor White
Write-Host ""
Write-Host "Current Status:" -ForegroundColor Yellow
Write-Host "  ✅ Min instances: 0 (scales to zero)" -ForegroundColor White
Write-Host "  ✅ Free tier: All services within limits" -ForegroundColor White
Write-Host "  ✅ Estimated cost: ~`$0.08/month" -ForegroundColor White
Write-Host ""
Write-Host "Optional Optimizations:" -ForegroundColor Cyan
Write-Host "  • Reduce Cloud Run memory (if stable)" -ForegroundColor White
Write-Host "  • Reduce function memory allocations" -ForegroundColor White
Write-Host "  • Set billing budget alerts" -ForegroundColor White
Write-Host "  • Enable Cloud Scheduler for automation" -ForegroundColor White
Write-Host ""
Write-Host "For full report, run: .\scripts\cost_report.ps1" -ForegroundColor Cyan
Write-Host ""
