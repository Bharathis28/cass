# Quick Test Reference

## Run All Tests
```bash
cd "c:\Users\Admin\New folder\cass"
py -m pytest scheduler/tests/ -v
```

## Run Specific Required Tests

### Test 1: Greenest Region Selection
```bash
py -m pytest scheduler/tests/test_carbon_fetcher.py::test_greenest_region_selection -v
```
✅ Verifies CarbonFetcher selects region with lowest carbon intensity (FI with 45 gCO₂/kWh)

### Test 2: HTTP 400 Error Handling
```bash
py -m pytest scheduler/tests/test_carbon_fetcher.py::test_fetch_carbon_handles_400 -v
```
✅ Verifies fetch_carbon_intensity returns None on 400 Bad Request

### Test 3: Retry Logic (3 attempts → fail)
```bash
py -m pytest scheduler/tests/test_job_runner.py::test_job_runner_retries_then_fails -v
```
✅ Verifies JobRunner makes exactly 3 retry attempts with 2-second delays before failing

## Test Summary
- **Total Tests:** 13
- **Required Tests:** 3 (all passing ✅)
- **Bonus Tests:** 10 (all passing ✅)
- **Execution Time:** ~3.3 seconds
- **Dependencies:** pytest, requests-mock

## Test Files
- `test_carbon_fetcher.py` - 6 tests for CarbonFetcher class
- `test_job_runner.py` - 7 tests for JobRunner class
- `conftest.py` - Shared pytest fixtures
- `README.md` - Complete documentation
- `TEST_IMPLEMENTATION_SUMMARY.md` - Implementation details
