"""
CASS-Lite v2 - Worker Cloud Function
=====================================
Google Cloud Function for Job Execution

This Cloud Function represents the actual workload that runs
in the carbon-optimal region selected by the scheduler.

In a real implementation, this would:
- Process data
- Run ML models
- Execute batch jobs
- Perform computations
- etc.

For CASS-Lite v2, it demonstrates the execution pattern.

Author: CASS-Lite v2 Team
Date: November 2025
"""

import json
import time
from datetime import datetime
import random
import functions_framework


@functions_framework.http
def run_worker_job(request):
    """
    HTTP Cloud Function entry point for worker job execution.
    
    This function is triggered by the job_runner after the scheduler
    selects the greenest region. It represents the actual workload.
    
    Args:
        request (flask.Request): The HTTP request object with payload:
            {
                'task_id': 'task_1762401063',
                'scheduled_at': '2025-11-06T...',
                'carbon_intensity': 42,
                'reason': 'carbon_optimized',
                'region': 'FI',
                'metadata': {...}
            }
        
    Returns:
        JSON response with execution results
        {
            'success': True,
            'task_id': 'task_1762401063',
            'region': 'FI',
            'execution_time_ms': 123,
            'status': 'completed',
            'message': 'Job executed successfully'
        }
    """
    start_time = time.time()
    
    print("="*75)
    print("⚡ CLOUD FUNCTION: run_worker_job")
    print("="*75)
    print(f"⏰ Started at: {datetime.now().isoformat()}")
    print(f"🔗 Request method: {request.method}")
    
    try:
        # Parse request payload
        request_json = request.get_json(silent=True)
        
        if not request_json:
            error_response = {
                'success': False,
                'error': 'No JSON payload provided',
                'message': '❌ Missing request payload',
                'cloud_function': 'run_worker_job'
            }
            print("❌ ERROR: No JSON payload")
            return (error_response, 400, {'Content-Type': 'application/json'})
        
        # Extract job details
        task_id = request_json.get('task_id', 'unknown')
        region = request_json.get('region', 'unknown')
        carbon_intensity = request_json.get('carbon_intensity', 0)
        scheduled_at = request_json.get('scheduled_at', 'N/A')
        reason = request_json.get('reason', 'N/A')
        metadata = request_json.get('metadata', {})
        
        # Region flags mapping
        region_flags = {
            'IN': '🇮🇳',
            'FI': '🇫🇮',
            'DE': '🇩🇪',
            'JP': '🇯🇵',
            'AU-NSW': '🇦🇺',
            'BR-CS': '🇧🇷'
        }
        region_flag = region_flags.get(region, '🌍')
        
        print("\n" + "="*75)
        print("📦 JOB DETAILS")
        print("="*75)
        print(f"📋 Task ID: {task_id}")
        print(f"🌍 Region: {region_flag} {region}")
        print(f"🌱 Carbon Intensity: {carbon_intensity} gCO₂/kWh")
        print(f"📅 Scheduled At: {scheduled_at}")
        print(f"💡 Reason: {reason}")
        print("="*75)
        
        # Simulate job execution
        print("\n🔄 Executing workload...")
        print(f"   → Running in region: {region_flag} {region}")
        print(f"   → Carbon-optimized execution")
        print(f"   → Using clean energy grid")
        
        # Simulate some processing time (0.5-2 seconds)
        import random
        processing_time = random.uniform(0.5, 2.0)
        time.sleep(processing_time)
        
        # Job completed successfully
        execution_time = round((time.time() - start_time) * 1000)
        
        response_data = {
            'success': True,
            'status': 'completed',
            'task_id': task_id,
            'region': region,
            'region_flag': region_flag,
            'carbon_intensity': carbon_intensity,
            'execution_time_ms': execution_time,
            'completed_at': datetime.now().isoformat(),
            'scheduled_at': scheduled_at,
            'reason': reason,
            'metadata': metadata,
            'message': f"✅ Job executed successfully in {region_flag} {region}",
            'cloud_function': 'run_worker_job'
        }
        
        print("\n" + "="*75)
        print("✅ JOB COMPLETED SUCCESSFULLY")
        print("="*75)
        print(f"📋 Task ID: {task_id}")
        print(f"🌍 Executed in: {region_flag} {region}")
        print(f"⏱️  Execution Time: {execution_time} ms")
        print(f"🌱 Carbon Used: {carbon_intensity} gCO₂/kWh")
        print("="*75)
        
        return (response_data, 200, {'Content-Type': 'application/json'})
    
    except Exception as e:
        execution_time = round((time.time() - start_time) * 1000)
        error_message = str(e)
        
        print(f"\n❌ ERROR: {error_message}")
        
        error_response = {
            'success': False,
            'status': 'error',
            'error': error_message,
            'execution_time_ms': execution_time,
            'message': '❌ Job execution failed',
            'cloud_function': 'run_worker_job',
            'failed_at': datetime.now().isoformat()
        }
        
        return (error_response, 500, {'Content-Type': 'application/json'})


# For local testing
if __name__ == '__main__':
    """
    Test the Cloud Function locally.
    """
    print("\n🧪 LOCAL TEST MODE")
    print("="*75)
    
    class MockRequest:
        """Mock Flask request object for testing."""
        method = 'POST'
        
        def get_json(self, silent=False):
            return {
                'task_id': 'test_task_12345',
                'region': 'FI',
                'carbon_intensity': 42,
                'scheduled_at': datetime.now().isoformat(),
                'reason': 'carbon_optimized',
                'metadata': {
                    'scheduler_version': 'CASS-Lite-v2',
                    'carbon_savings_gco2': 230
                }
            }
    
    # Run function - type ignore for mock request
    response, status_code, headers = run_worker_job(MockRequest())  # type: ignore[arg-type]
    
    print(f"\n📤 Response (Status {status_code}):")
    print(json.dumps(json.loads(response), indent=2))
