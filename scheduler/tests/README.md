# Scheduler Unit Tests

## Overview
This directory contains unit tests for the CASS-Lite v2 scheduler components using pytest and requests-mock.

## Test Files

### `test_carbon_fetcher.py`
Tests for the `CarbonFetcher` class that fetches carbon intensity data from ElectricityMap API.

**Tests:**
- ✅ `test_greenest_region_selection()` - Verifies correct selection of the region with lowest carbon intensity
- ✅ `test_fetch_carbon_handles_400()` - Tests error handling for HTTP 400 Bad Request
- ✅ `test_fetch_carbon_success()` - Tests successful data fetch and caching
- ✅ `test_fetch_carbon_handles_401()` - Tests authentication error handling
- ✅ `test_fetch_carbon_handles_429()` - Tests rate limit error handling
- ✅ `test_fetch_carbon_handles_timeout()` - Tests network timeout handling

### `test_job_runner.py`
Tests for the `JobRunner` class that triggers Cloud Functions with retry logic.

**Tests:**
- ✅ `test_job_runner_retries_then_fails()` - Verifies retry mechanism (3 attempts → fail)
- ✅ `test_trigger_function_success()` - Tests successful Cloud Function invocation
- ✅ `test_trigger_function_connection_error()` - Tests connection error handling
- ✅ `test_trigger_function_timeout()` - Tests timeout error handling
- ✅ `test_trigger_function_eventual_success()` - Tests eventual success after retries
- ✅ `test_get_function_url()` - Tests URL retrieval from config
- ✅ `test_authentication_enabled()` - Tests OAuth2 authentication headers

## Running Tests

### Install Dependencies
```bash
# Install test dependencies
pip install -r requirements.txt

# Or install specific test packages
pip install pytest requests-mock
```

### Run All Tests
```bash
# Run all tests with verbose output
pytest scheduler/tests/ -v

# Run with coverage
pytest scheduler/tests/ --cov=scheduler --cov-report=html

# Run specific test file
pytest scheduler/tests/test_carbon_fetcher.py -v

# Run specific test function
pytest scheduler/tests/test_job_runner.py::test_job_runner_retries_then_fails -v
```

### Run Tests in Quiet Mode
```bash
pytest scheduler/tests/ -q
```

### Run Tests with Print Statements
```bash
pytest scheduler/tests/ -s
```

## Test Coverage

### CarbonFetcher Coverage
- ✅ API response parsing
- ✅ Error handling (400, 401, 429, timeout)
- ✅ Caching mechanism
- ✅ Multi-region data fetching
- ✅ Greenest region selection algorithm

### JobRunner Coverage
- ✅ Cloud Function HTTP invocation
- ✅ Retry logic (max 3 attempts, 2 second delay)
- ✅ OAuth2 authentication headers
- ✅ Error handling (500, timeout, connection errors)
- ✅ Response validation
- ✅ URL configuration

## Test Strategy

### Mocking
All tests use `requests-mock` to simulate HTTP responses:
- **ElectricityMap API**: Mocked to return controlled carbon intensity data
- **Cloud Function endpoints**: Mocked to simulate success/failure scenarios
- **time.sleep**: Patched to avoid actual delays during testing

### Fixtures (conftest.py)
Shared test data available across all tests:
- `sample_carbon_data`: Mock carbon intensity responses
- `sample_job_runner_config`: JobRunner configuration
- `sample_job_payload`: Cloud Function payload
- `mock_api_key`: Test API key

## Test Requirements
- Python 3.9+
- pytest 7.4.3+
- requests-mock 1.11.0+
- requests 2.31.0+

## CI/CD Integration
These tests can be integrated into GitHub Actions workflow:

```yaml
- name: Run Unit Tests
  run: |
    pytest scheduler/tests/ -v --cov=scheduler --cov-report=xml

- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage.xml
```

## Expected Output

```
==================== test session starts ====================
collected 13 items

scheduler/tests/test_carbon_fetcher.py::test_greenest_region_selection PASSED [ 7%]
scheduler/tests/test_carbon_fetcher.py::test_fetch_carbon_handles_400 PASSED [15%]
scheduler/tests/test_carbon_fetcher.py::test_fetch_carbon_success PASSED [23%]
scheduler/tests/test_carbon_fetcher.py::test_fetch_carbon_handles_401 PASSED [30%]
scheduler/tests/test_carbon_fetcher.py::test_fetch_carbon_handles_429 PASSED [38%]
scheduler/tests/test_carbon_fetcher.py::test_fetch_carbon_handles_timeout PASSED [46%]

scheduler/tests/test_job_runner.py::test_job_runner_retries_then_fails PASSED [53%]
scheduler/tests/test_job_runner.py::test_trigger_function_success PASSED [61%]
scheduler/tests/test_job_runner.py::test_trigger_function_connection_error PASSED [69%]
scheduler/tests/test_job_runner.py::test_trigger_function_timeout PASSED [76%]
scheduler/tests/test_job_runner.py::test_trigger_function_eventual_success PASSED [84%]
scheduler/tests/test_job_runner.py::test_get_function_url PASSED [92%]
scheduler/tests/test_job_runner.py::test_authentication_enabled PASSED [100%]

==================== 13 passed in 2.45s ====================
```

## Troubleshooting

### Import Errors
If you see import errors, ensure you're running pytest from the project root:
```bash
cd "c:\Users\Admin\New folder\cass"
pytest scheduler/tests/ -v
```

### Module Not Found
Install dependencies:
```bash
pip install -r requirements.txt
```

### Permission Errors
Run with appropriate permissions or use a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
pytest scheduler/tests/ -v
```
