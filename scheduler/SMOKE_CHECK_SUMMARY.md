# Smoke Check Implementation Summary

## ✅ Task Completed

Successfully created `scheduler/smoke_check.py` that performs a comprehensive dry-run of the CASS-Lite v2 scheduler workflow.

## 📋 Requirements Met

### ✅ Imports CarbonFetcher and CarbonScheduler
```python
from carbon_fetcher import CarbonFetcher
from main import CarbonScheduler
```

### ✅ Runs Full Dry-Run Cycle
1. **Fetch** - Retrieves real-time carbon intensity from 6 regions (IN, FI, DE, JP, AU-NSW, BR-CS)
2. **Select** - Identifies greenest region with lowest carbon intensity
3. **Prepare Job** - Generates job instructions with task ID, Cloud Function URL, and payload
4. **Skip Actual POST** - Does NOT invoke Cloud Functions (dry-run mode)

### ✅ Prints Selected Region & Savings
```
📊 SELECTED GREENEST REGION:
   Region: 🇫🇮 Finland (FI)
   Carbon Intensity: 73 gCO₂/kWh
   Average Carbon (all regions): 354 gCO₂/kWh
   Carbon Savings: 281 gCO₂/kWh
   Savings Percentage: 79.4%
```

### ✅ Exit Codes
- `0` - Success: All checks passed ✅
- `1` - Failure: Carbon data fetch failed
- `2` - Failure: Decision making failed
- `3` - Failure: Job preparation failed
- `4` - Failure: Unexpected exception

### ✅ Try/Except Error Handling
All steps wrapped in comprehensive try/except blocks:
```python
try:
    scheduler = CarbonScheduler(config_path=config_path)
    print_success("CarbonScheduler initialized successfully")
except Exception as e:
    print_error(f"Failed to initialize scheduler: {e}")
    print(f"   Exception type: {type(e).__name__}")
    print(f"   Exception details: {str(e)[:200]}")
    return 4
```

### ✅ Folder Structure Unchanged
Only added new files to `scheduler/` directory:
```
scheduler/
├── carbon_fetcher.py (existing)
├── main.py (existing)
├── job_runner.py (existing)
├── config.json (existing)
├── firestore_logger.py (existing)
├── smoke_check.py ← NEW
├── SMOKE_CHECK_DOCUMENTATION.md ← NEW
├── SMOKE_CHECK_QUICK_REFERENCE.md ← NEW
└── tests/ (existing)
```

## 🎯 Workflow Steps

### Step 1: Verify Imports
- ✅ CarbonFetcher imported
- ✅ CarbonScheduler imported
- ✅ JobRunner imported

### Step 2: Initialize Scheduler
- ✅ Loads config.json
- ✅ Initializes CarbonFetcher with API key
- ✅ Initializes JobRunner with retry logic (max_retries=3, retry_delay=2s)
- ✅ Initializes Firestore logger (gracefully handles connection failures)

### Step 3: Fetch Carbon Data & Make Decision
- ✅ Calls `scheduler.make_decision()`
- ✅ Fetches real-time data from ElectricityMap API for 6 regions
- ✅ Selects region with lowest carbon intensity
- ✅ Calculates carbon savings vs average

### Step 4: Display Decision Results
- ✅ Selected region (name, flag, code)
- ✅ Carbon intensity (gCO₂/kWh)
- ✅ Carbon savings (absolute and percentage)
- ✅ Regions analyzed count
- ✅ Decision time (ms)

### Step 5: Prepare Job Instructions (Dry-Run)
- ✅ Calls `scheduler.prepare_job_instructions()`
- ✅ Generates task ID
- ✅ Retrieves Cloud Function URL
- ✅ Prepares payload with carbon data
- ✅ **SKIPS** actual HTTP POST request

### Step 6: Verify Calculations
- ✅ Validates carbon savings calculation
- ✅ Verifies savings percentage
- ✅ Checks consistency

## 📊 Test Results

### Successful Execution
```
$ cd scheduler
$ py smoke_check.py

================================================================================
🧪 CASS-LITE v2 SMOKE CHECK - DRY RUN MODE
================================================================================
⏰ Started at: 2025-11-11 14:51:27
🔍 Mode: Dry-run (no actual Cloud Function calls will be made)
================================================================================

[... detailed output ...]

✅ ALL CHECKS PASSED!

📊 Summary:
   ✓ Imports verified
   ✓ Scheduler initialized
   ✓ Carbon data fetched (6 regions)
   ✓ Greenest region selected: Finland (FI)
   ✓ Carbon savings calculated: 281 gCO₂/kWh (79.4%)
   ✓ Job instructions prepared (dry-run)
   ✓ Calculations verified

================================================================================
🎉 SMOKE CHECK COMPLETED SUCCESSFULLY
================================================================================
⏰ Finished at: 2025-11-11 14:51:37
================================================================================

Exit code: 0
```

**Execution Time:** ~10 seconds  
**Exit Code:** 0 (Success)  
**Regions Checked:** 6  
**Carbon Savings:** 281 gCO₂/kWh (79.4%)

## 🔧 Usage

### Basic Run
```bash
cd scheduler
python smoke_check.py
```

### With Exit Code Check
```powershell
cd scheduler
py smoke_check.py
echo "Exit code: $LASTEXITCODE"
```

### In CI/CD Pipeline
```bash
cd scheduler
python smoke_check.py
if [ $? -eq 0 ]; then
  echo "✅ Smoke check passed - proceeding with deployment"
else
  echo "❌ Smoke check failed - deployment cancelled"
  exit 1
fi
```

## 📝 Key Features

### ✅ Safe Dry-Run Mode
- No actual Cloud Function HTTP POST requests
- No Firestore writes (console-only mode if DB unavailable)
- Only fetches carbon data from ElectricityMap API

### ✅ Real Carbon Data
- Live API calls to ElectricityMap
- Real-time carbon intensity for 6 regions
- Actual greenest region selection

### ✅ Comprehensive Validation
- ✅ Import verification
- ✅ Configuration loading
- ✅ API connectivity
- ✅ Decision logic
- ✅ Calculation accuracy
- ✅ Job preparation

### ✅ Detailed Error Reporting
```python
try:
    decision = scheduler.make_decision()
except Exception as e:
    print_error(f"Failed to make scheduling decision: {e}")
    print(f"   Exception type: {type(e).__name__}")
    print(f"   Exception details: {str(e)[:200]}")
    return 2
```

### ✅ Clear Output
- Step-by-step progress
- Success/failure indicators (✅/❌)
- Detailed decision data
- Final summary report

## 📦 Files Created

1. **`scheduler/smoke_check.py`** (287 lines)
   - Main smoke check script
   - Comprehensive dry-run workflow
   - Exit codes 0-4 for different failure modes

2. **`scheduler/SMOKE_CHECK_DOCUMENTATION.md`** (400+ lines)
   - Complete documentation
   - Usage examples
   - Error handling guide
   - CI/CD integration

3. **`scheduler/SMOKE_CHECK_QUICK_REFERENCE.md`** (50 lines)
   - Quick reference card
   - Common commands
   - Exit code summary

## 🎉 Success Criteria

✅ **Imports CarbonFetcher and CarbonScheduler** - Both imported successfully  
✅ **Runs full dry-run cycle** - Fetch → Select → Prepare → Skip POST  
✅ **Prints greenest region** - Finland (FI) with 73 gCO₂/kWh  
✅ **Prints computed savings** - 281 gCO₂/kWh (79.4%)  
✅ **Exits with code 0 on success** - Verified ✅  
✅ **Exits nonzero on failure** - Codes 1-4 for different failures  
✅ **Uses try/except** - All steps wrapped in error handling  
✅ **Logs meaningful errors** - Exception type, message, and details  
✅ **Folder structure unchanged** - Only added files to scheduler/  

## 🚀 Next Steps

### Run It
```bash
cd scheduler
py smoke_check.py
```

### Integrate with CI/CD
Add to `.github/workflows/test.yml`:
```yaml
- name: Run Smoke Check
  run: |
    cd scheduler
    python smoke_check.py
```

### Pre-deployment Validation
```bash
# Before deploying to production
cd scheduler
python smoke_check.py && gcloud functions deploy ... || exit 1
```

---

**Status:** ✅ COMPLETE  
**Date:** November 11, 2025  
**Execution Time:** ~10 seconds  
**Exit Code:** 0 (Success)
