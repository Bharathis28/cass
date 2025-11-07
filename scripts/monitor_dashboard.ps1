# ============================================================================
# CASS-Lite v2 - Cloud Monitoring & Observability Script
# ============================================================================
# Purpose: Real-time monitoring for Cloud Run dashboard and Cloud Functions
# Author: Auto-generated for CASS-Lite v2 project
# Date: November 7, 2025
# ============================================================================

param(
    [switch]$Logs,
    [switch]$Errors,
    [switch]$Metrics,
    [switch]$Status,
    [switch]$Stream,
    [switch]$All
)

$PROJECT_ID = "cass-lite"
$REGION = "asia-south1"
$DASHBOARD_SERVICE = "cass-lite-dashboard"

# Color output helpers
function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host $Text -ForegroundColor Cyan
    Write-Host "============================================================================" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Text)
    Write-Host "✅ $Text" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Text)
    Write-Host "⚠️  $Text" -ForegroundColor Yellow
}

function Write-Error-Custom {
    param([string]$Text)
    Write-Host "❌ $Text" -ForegroundColor Red
}

function Write-Info {
    param([string]$Text)
    Write-Host "ℹ️  $Text" -ForegroundColor White
}

# ============================================================================
# FUNCTION: Get Service Status
# ============================================================================
function Get-ServiceStatus {
    Write-Header "SERVICE STATUS - Cloud Run and Cloud Functions"
    
    Write-Host ""
    Write-Host "📊 Cloud Run Service: $DASHBOARD_SERVICE" -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    
    $status = gcloud run services describe $DASHBOARD_SERVICE `
        --region=$REGION `
        --project=$PROJECT_ID `
        --format="table(status.url,status.conditions[0].status,metadata.annotations.'serving.knative.dev/creator',metadata.creationTimestamp)" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host $status
        Write-Success "Dashboard service is active"
    } else {
        Write-Error-Custom "Failed to get dashboard status"
    }
    
    Write-Host ""
    Write-Host "⚡ Cloud Functions Status" -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    
    $functions = @("run_scheduler", "run_worker_job")
    foreach ($func in $functions) {
        $funcStatus = gcloud functions describe $func `
            --region=$REGION `
            --project=$PROJECT_ID `
            --format="value(state)" 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            if ($funcStatus -eq "ACTIVE") {
                Write-Success "$func : $funcStatus"
            } else {
                Write-Warning "$func : $funcStatus"
            }
        } else {
            Write-Error-Custom "Failed to get status for $func"
        }
    }
}

# ============================================================================
# FUNCTION: Get Recent Logs
# ============================================================================
function Get-RecentLogs {
    Write-Header "RECENT LOGS - Last 10 Entries"
    
    Write-Host ""
    Write-Host "📝 Dashboard Logs (Cloud Run)" -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    
    gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=$DASHBOARD_SERVICE" `
        --limit=10 `
        --format="table(timestamp,severity,textPayload.extract(0,100))" `
        --project=$PROJECT_ID
    
    Write-Host ""
    Write-Host "📝 Cloud Functions Logs" -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    
    gcloud logging read "resource.type=cloud_function AND (resource.labels.function_name=run_scheduler OR resource.labels.function_name=run_worker_job)" `
        --limit=10 `
        --format="table(timestamp,resource.labels.function_name,severity,textPayload.extract(0,80))" `
        --project=$PROJECT_ID
}

# ============================================================================
# FUNCTION: Get Error Logs
# ============================================================================
function Get-ErrorLogs {
    Write-Header "ERROR LOGS - Critical Issues"
    
    Write-Host ""
    Write-Host "🚨 Dashboard Errors (Last 24 hours)" -ForegroundColor Red
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    
    $dashboardErrors = gcloud logging read "severity>=ERROR AND resource.type=cloud_run_revision AND resource.labels.service_name=$DASHBOARD_SERVICE" `
        --limit=10 `
        --format="table(timestamp,severity,textPayload.extract(0,150))" `
        --project=$PROJECT_ID `
        --freshness=24h 2>&1
    
    if ($dashboardErrors -match "Listed 0 items") {
        Write-Success "No errors in the last 24 hours!"
    } else {
        Write-Host $dashboardErrors
    }
    
    Write-Host ""
    Write-Host "🚨 Cloud Functions Errors (Last 24 hours)" -ForegroundColor Red
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    
    $functionErrors = gcloud logging read "severity>=ERROR AND resource.type=cloud_function" `
        --limit=10 `
        --format="table(timestamp,resource.labels.function_name,severity)" `
        --project=$PROJECT_ID `
        --freshness=24h 2>&1
    
    if ($functionErrors -match "Listed 0 items") {
        Write-Success "No errors in the last 24 hours!"
    } else {
        Write-Host $functionErrors
    }
}

# ============================================================================
# FUNCTION: Get Metrics
# ============================================================================
function Get-Metrics {
    Write-Header "RESOURCE METRICS - CPU, Memory, Requests"
    
    Write-Host ""
    Write-Host "📈 Cloud Run Metrics (Last Hour)" -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    
    # Get request count
    Write-Info "Request Count:"
    gcloud monitoring time-series list `
        --filter="metric.type=run.googleapis.com/request_count AND resource.labels.service_name=$DASHBOARD_SERVICE" `
        --format="table(points[0].value.int64Value)" `
        --project=$PROJECT_ID `
        2>&1 | Select-Object -First 5
    
    # CPU usage
    Write-Host ""
    Write-Info "CPU Utilization:"
    gcloud monitoring time-series list `
        --filter="metric.type=run.googleapis.com/container/cpu/utilizations AND resource.labels.service_name=$DASHBOARD_SERVICE" `
        --format="table(points[0].value.doubleValue)" `
        --project=$PROJECT_ID `
        2>&1 | Select-Object -First 5
    
    # Memory usage
    Write-Host ""
    Write-Info "Memory Utilization:"
    gcloud monitoring time-series list `
        --filter="metric.type=run.googleapis.com/container/memory/utilizations AND resource.labels.service_name=$DASHBOARD_SERVICE" `
        --format="table(points[0].value.doubleValue)" `
        --project=$PROJECT_ID `
        2>&1 | Select-Object -First 5
    
    Write-Host ""
    Write-Host "💡 Tip: For detailed metrics, visit:" -ForegroundColor Cyan
    Write-Host "   https://console.cloud.google.com/run/detail/$REGION/$DASHBOARD_SERVICE/metrics?project=$PROJECT_ID" -ForegroundColor White
}

# ============================================================================
# FUNCTION: Stream Logs (Real-time)
# ============================================================================
function Stream-Logs {
    Write-Header "LIVE LOG STREAM - Press Ctrl+C to stop"
    
    Write-Host ""
    Write-Info "Streaming logs from: $DASHBOARD_SERVICE"
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    Write-Host ""
    
    gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=$DASHBOARD_SERVICE" `
        --project=$PROJECT_ID `
        --format="table(timestamp,severity,textPayload)"
}

# ============================================================================
# FUNCTION: Health Check
# ============================================================================
function Get-HealthCheck {
    Write-Header "HEALTH CHECK - Service Availability"
    
    Write-Host ""
    Write-Info "Testing dashboard endpoint..."
    
    $url = gcloud run services describe $DASHBOARD_SERVICE `
        --region=$REGION `
        --project=$PROJECT_ID `
        --format="value(status.url)" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   URL: $url" -ForegroundColor White
        
        try {
            $response = Invoke-WebRequest -Uri "$url/_stcore/health" -Method Get -TimeoutSec 10 -UseBasicParsing 2>&1
            if ($response.StatusCode -eq 200) {
                Write-Success "Dashboard is HEALTHY (HTTP 200)"
            } else {
                Write-Warning "Dashboard returned HTTP $($response.StatusCode)"
            }
        } catch {
            Write-Warning "Health check endpoint not accessible (normal for Streamlit)"
            Write-Info "Testing main page instead..."
            
            try {
                $mainResponse = Invoke-WebRequest -Uri $url -Method Head -TimeoutSec 10 -UseBasicParsing 2>&1
                if ($mainResponse.StatusCode -eq 200) {
                    Write-Success "Dashboard main page is accessible (HTTP 200)"
                }
            } catch {
                Write-Error-Custom "Dashboard is not accessible: $_"
            }
        }
    } else {
        Write-Error-Custom "Failed to get service URL"
    }
}

# ============================================================================
# FUNCTION: Full Report
# ============================================================================
function Get-FullReport {
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host "             CASS-Lite v2 - MONITORING DASHBOARD                        " -ForegroundColor Cyan
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Project: $PROJECT_ID" -ForegroundColor White
    Write-Host "Region: $REGION" -ForegroundColor White
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "Timestamp: $timestamp" -ForegroundColor White
    
    Get-HealthCheck
    Get-ServiceStatus
    Get-RecentLogs
    Get-ErrorLogs
    Get-Metrics
    
    Write-Header "QUICK LINKS"
    Write-Host ""
    Write-Info "Cloud Run Console:"
    Write-Host "   https://console.cloud.google.com/run/detail/$REGION/$DASHBOARD_SERVICE?project=$PROJECT_ID" -ForegroundColor White
    Write-Host ""
    Write-Info "Cloud Logging Console:"
    Write-Host "   https://console.cloud.google.com/logs/query?project=$PROJECT_ID" -ForegroundColor White
    Write-Host ""
    Write-Info "Cloud Monitoring Console:"
    Write-Host "   https://console.cloud.google.com/monitoring?project=$PROJECT_ID" -ForegroundColor White
    Write-Host ""
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if ($All) {
    Get-FullReport
}
elseif ($Status) {
    Get-ServiceStatus
    Get-HealthCheck
}
elseif ($Logs) {
    Get-RecentLogs
}
elseif ($Errors) {
    Get-ErrorLogs
}
elseif ($Metrics) {
    Get-Metrics
}
elseif ($Stream) {
    Stream-Logs
}
else {
    # Default: Show usage
    Write-Host ""
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host "         CASS-Lite v2 - Monitoring Script                               " -ForegroundColor Cyan
    Write-Host "============================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\monitor_dashboard.ps1 [OPTION]" -ForegroundColor White
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor Yellow
    Write-Host "  -All        Show complete monitoring report (recommended)" -ForegroundColor White
    Write-Host "  -Status     Service status and health check" -ForegroundColor White
    Write-Host "  -Logs       Recent logs from all services" -ForegroundColor White
    Write-Host "  -Errors     Error logs (last 24 hours)" -ForegroundColor White
    Write-Host "  -Metrics    CPU, memory, and request metrics" -ForegroundColor White
    Write-Host "  -Stream     Live log streaming (Ctrl+C to stop)" -ForegroundColor White
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Yellow
    Write-Host "  .\monitor_dashboard.ps1 -All      # Full monitoring report" -ForegroundColor Gray
    Write-Host "  .\monitor_dashboard.ps1 -Errors   # Check for errors" -ForegroundColor Gray
    Write-Host "  .\monitor_dashboard.ps1 -Stream   # Real-time logs" -ForegroundColor Gray
    Write-Host ""
}
