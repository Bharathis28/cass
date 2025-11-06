"""
CASS-Lite v2 - Scheduler Cloud Function
========================================
Google Cloud Function for Carbon-Aware Scheduling

This Cloud Function triggers the complete scheduling cycle:
1. Fetch carbon intensity data from multiple regions
2. Select the greenest region
3. Trigger worker job in that region
4. Log the decision to Firestore

Can be triggered via HTTP or Cloud Scheduler (cron).

Author: CASS-Lite v2 Team
Date: November 2025
"""

import json
import sys
import os
from datetime import datetime

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../scheduler'))

from main import CarbonScheduler


def run_scheduler(request):
    """
    HTTP Cloud Function entry point for scheduling.
    
    This function is triggered via HTTP POST and runs a complete
    carbon-aware scheduling cycle.
    
    Args:
        request (flask.Request): The HTTP request object
        
    Returns:
        JSON response with scheduling results
        {
            'success': True,
            'region': 'FI',
            'region_name': 'Finland',
            'carbon_intensity': 42,
            'savings_gco2': 230,
            'timestamp': '2025-11-06T...',
            'message': 'Scheduling cycle completed'
        }
    """
    print("="*75)
    print("🚀 CLOUD FUNCTION: run_scheduler")
    print("="*75)
    print(f"⏰ Triggered at: {datetime.now().isoformat()}")
    print(f"🔗 Request method: {request.method}")
    
    try:
        # Get request data (if any)
        request_json = request.get_json(silent=True)
        print(f"📦 Request payload: {request_json if request_json else 'None'}")
        
        # Initialize scheduler
        print("\n📋 Initializing Carbon Scheduler...")
        scheduler = CarbonScheduler(config_path='../../scheduler/config.json')
        
        # Run scheduling cycle
        print("\n🔄 Running scheduling cycle...")
        success = scheduler.run_scheduling_cycle()
        
        if success and scheduler.last_decision:
            decision = scheduler.last_decision
            
            response_data = {
                'success': True,
                'status': 'completed',
                'decision': {
                    'region': decision.get('selected_region'),
                    'region_name': decision.get('region_name'),
                    'region_flag': decision.get('region_flag'),
                    'carbon_intensity': decision.get('carbon_intensity'),
                    'savings_gco2': decision.get('savings_gco2'),
                    'savings_percent': decision.get('savings_percent'),
                    'decision_time_ms': decision.get('decision_time_ms'),
                    'timestamp': decision.get('timestamp')
                },
                'message': f"✅ Scheduled job in {decision.get('region_name')} ({decision.get('carbon_intensity')} gCO₂/kWh)",
                'cloud_function': 'run_scheduler',
                'triggered_at': datetime.now().isoformat()
            }
            
            print("\n" + "="*75)
            print("✅ CLOUD FUNCTION COMPLETED SUCCESSFULLY")
            print("="*75)
            print(f"🌱 Selected Region: {decision.get('region_flag')} {decision.get('selected_region')}")
            print(f"⚡ Carbon Intensity: {decision.get('carbon_intensity')} gCO₂/kWh")
            print(f"💰 Carbon Savings: {decision.get('savings_gco2')} gCO₂/kWh")
            print("="*75)
            
            return json.dumps(response_data), 200, {'Content-Type': 'application/json'}
        
        else:
            response_data = {
                'success': False,
                'status': 'failed',
                'message': '❌ Scheduling cycle failed',
                'cloud_function': 'run_scheduler',
                'triggered_at': datetime.now().isoformat()
            }
            
            print("\n" + "="*75)
            print("❌ CLOUD FUNCTION FAILED")
            print("="*75)
            
            return json.dumps(response_data), 500, {'Content-Type': 'application/json'}
    
    except Exception as e:
        error_message = str(e)
        print(f"\n❌ ERROR: {error_message}")
        
        response_data = {
            'success': False,
            'status': 'error',
            'error': error_message,
            'message': '❌ Unexpected error in scheduling',
            'cloud_function': 'run_scheduler',
            'triggered_at': datetime.now().isoformat()
        }
        
        return json.dumps(response_data), 500, {'Content-Type': 'application/json'}


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
            return {'test': True}
    
    # Run function
    response, status_code, headers = run_scheduler(MockRequest())
    
    print(f"\n📤 Response (Status {status_code}):")
    print(json.dumps(json.loads(response), indent=2))
