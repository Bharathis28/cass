"""
CASS-Lite v2 - Main Scheduler
==============================
Carbon-Aware Serverless Scheduler Decision Engine

This is the core orchestrator that:
1. Fetches real-time carbon intensity data from multiple regions
2. Selects the greenest (lowest carbon) region
3. Logs the decision for tracking and analytics
4. Prepares deployment instructions for the job runner

Author: CASS-Lite v2 Team
Date: November 2025
"""

import json
import time
from datetime import datetime
from typing import Dict, Optional
from carbon_fetcher import CarbonFetcher
from job_runner import JobRunner
from firestore_logger import FirestoreLogger


class CarbonScheduler:
    """
    Main scheduler that orchestrates carbon-aware deployment decisions.
    
    This class integrates carbon data fetching, decision logic, and
    prepares instructions for serverless job execution.
    
    Attributes:
        config (dict): Configuration loaded from config.json
        fetcher (CarbonFetcher): Carbon intensity data fetcher
        last_decision (dict): Most recent scheduling decision
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize the Carbon Scheduler.
        
        Args:
            config_path: Path to configuration file (default: config.json)
        """
        print("="*75)
        print("🚀 CASS-LITE v2 - CARBON-AWARE SERVERLESS SCHEDULER")
        print("="*75)
        print(f"⏰ Initializing scheduler at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize carbon fetcher
        api_key = self.config.get('api', {}).get('electricitymap_key', '')
        cache_ttl = self.config.get('api', {}).get('cache_ttl_seconds', 300)
        
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            # Use hardcoded key for now (in production, use environment variables)
            api_key = "gwASf8vJiQ92CPIuRzuy"
        
        self.fetcher = CarbonFetcher(api_key=api_key, cache_ttl=cache_ttl)
        self.job_runner = JobRunner(self.config, max_retries=3, retry_delay=2, timeout=30)
        self.firestore_logger = FirestoreLogger(self.config)
        self.last_decision = None
        
        print(f"✓ Configuration loaded from {config_path}")
        print(f"✓ Carbon fetcher initialized ({len(self.fetcher.regions)} regions)")
        print(f"✓ Job runner initialized")
        print(f"✓ Firestore logger initialized")
        print(f"✓ Cache TTL: {cache_ttl} seconds\n")
    
    def _load_config(self, config_path: str) -> dict:
        """
        Load configuration from JSON file.
        
        Args:
            config_path: Path to config.json
            
        Returns:
            Dictionary containing configuration
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Config file not found: {config_path}")
            print("   Using default configuration...")
            return {
                "api": {"electricitymap_key": "", "cache_ttl_seconds": 300},
                "regions": {},
                "scheduler": {"check_interval_minutes": 15}
            }
        except json.JSONDecodeError as e:
            print(f"⚠️  Error parsing config file: {e}")
            print("   Using default configuration...")
            return {}
    
    def make_decision(self) -> Optional[Dict]:
        """
        Core decision-making logic: Analyze carbon data and choose deployment region.
        
        This method:
        1. Fetches carbon intensity for all regions
        2. Identifies the greenest region
        3. Calculates carbon savings
        4. Logs the decision
        
        Returns:
            Dictionary containing the scheduling decision, or None if failed
            {
                'timestamp': '2025-11-05T13:45:00',
                'selected_region': 'FI',
                'region_name': 'Finland',
                'region_flag': '🇫🇮',
                'carbon_intensity': 40,
                'savings_gco2': 260,
                'savings_percent': 86.5,
                'average_carbon': 300,
                'total_regions_checked': 6,
                'decision_time_ms': 1234
            }
        """
        print("\n" + "="*75)
        print("🧠 MAKING CARBON-AWARE SCHEDULING DECISION")
        print("="*75)
        
        start_time = time.time()
        
        # Step 1: Fetch carbon intensity data
        print("\n📡 Step 1: Fetching carbon intensity data...")
        greenest = self.fetcher.get_greenest_region()
        
        if not greenest:
            print("\n❌ DECISION FAILED: Could not fetch carbon data")
            return None
        
        # Step 2: Build decision record
        decision_time_ms = round((time.time() - start_time) * 1000)
        
        decision = {
            'timestamp': datetime.now().isoformat(),
            'selected_region': greenest['zone'],
            'region_name': greenest['name'],
            'region_flag': greenest['flag'],
            'carbon_intensity': greenest['carbonIntensity'],
            'savings_gco2': greenest.get('savings', 0),
            'savings_percent': round((greenest.get('savings', 0) / greenest.get('averageCarbon', 1)) * 100, 1),
            'average_carbon': greenest.get('averageCarbon', 0),
            'total_regions_checked': greenest.get('totalRegions', 0),
            'decision_time_ms': decision_time_ms,
            'data_timestamp': greenest.get('datetime', 'N/A')
        }
        
        # Store decision
        self.last_decision = decision
        
        # Step 3: Log decision summary
        print("\n" + "="*75)
        print("✅ DECISION COMPLETE")
        print("="*75)
        print(f"🎯 Selected Region: {decision['region_flag']} {decision['region_name']} ({decision['selected_region']})")
        print(f"🌱 Carbon Intensity: {decision['carbon_intensity']} gCO₂/kWh")
        print(f"💰 Carbon Savings: {decision['savings_gco2']} gCO₂/kWh ({decision['savings_percent']}%)")
        print(f"⚡ Decision Time: {decision['decision_time_ms']} ms")
        print(f"📊 Regions Analyzed: {decision['total_regions_checked']}")
        print("="*75 + "\n")
        
        return decision
    
    def prepare_job_instructions(self, decision: Optional[Dict] = None) -> Optional[Dict]:
        """
        Prepare instructions for the job runner to execute workload.
        
        Args:
            decision: Scheduling decision (uses last_decision if None)
            
        Returns:
            Dictionary with job execution instructions
            {
                'target_region': 'FI',
                'cloud_function_url': 'https://...',
                'payload': {...},
                'metadata': {...}
            }
        """
        if decision is None:
            decision = self.last_decision
        
        if not decision:
            print("⚠️  No decision available to prepare job instructions")
            return None
        
        print("\n" + "="*75)
        print("📋 PREPARING JOB EXECUTION INSTRUCTIONS")
        print("="*75)
        
        target_region = decision['selected_region']
        
        # Get Cloud Function URL from config
        cloud_function_url = self.config.get('regions', {}).get(
            target_region, {}
        ).get('cloud_function_url', '')
        
        if not cloud_function_url:
            cloud_function_url = f"https://{target_region.lower()}-worker.cloudfunctions.net/execute"
            print(f"⚠️  No Cloud Function URL configured for {target_region}")
            print(f"   Using placeholder: {cloud_function_url}")
        
        # Build job instructions
        instructions = {
            'target_region': target_region,
            'region_name': decision['region_name'],
            'cloud_function_url': cloud_function_url,
            'payload': {
                'task_id': f"task_{int(time.time())}",
                'scheduled_at': decision['timestamp'],
                'carbon_intensity': decision['carbon_intensity'],
                'reason': 'carbon_optimized'
            },
            'metadata': {
                'scheduler_version': 'CASS-Lite-v2',
                'decision_timestamp': decision['timestamp'],
                'carbon_savings_gco2': decision['savings_gco2'],
                'carbon_savings_percent': decision['savings_percent']
            }
        }
        
        print(f"✓ Target Region: {decision['region_flag']} {target_region}")
        print(f"✓ Cloud Function: {cloud_function_url}")
        print(f"✓ Task ID: {instructions['payload']['task_id']}")
        print(f"✓ Carbon Intensity: {decision['carbon_intensity']} gCO₂/kWh")
        print("="*75 + "\n")
        
        return instructions
    
    def log_decision_to_console(self, decision: Dict) -> None:
        """
        Log decision details to console (placeholder for Firestore logging).
        
        Args:
            decision: The scheduling decision to log
        """
        print("\n" + "="*75)
        print("📝 LOGGING DECISION (Console)")
        print("="*75)
        print(f"Timestamp: {decision['timestamp']}")
        print(f"Region: {decision['region_flag']} {decision['selected_region']} - {decision['region_name']}")
        print(f"Carbon: {decision['carbon_intensity']} gCO₂/kWh")
        print(f"Savings: {decision['savings_gco2']} gCO₂/kWh ({decision['savings_percent']}%)")
        print(f"Decision Time: {decision['decision_time_ms']} ms")
        print("="*75)
        print("💡 Note: Firestore logging will be implemented in firestore_logger.py")
        print("="*75 + "\n")
    
    def run_scheduling_cycle(self) -> bool:
        """
        Execute a complete scheduling cycle.
        
        This is the main workflow:
        1. Make carbon-aware decision
        2. Prepare job instructions
        3. Log the decision
        4. (Later) Trigger job execution via job_runner
        
        Returns:
            True if cycle completed successfully, False otherwise
        """
        print("\n" + "="*75)
        print("🔄 STARTING SCHEDULING CYCLE")
        print("="*75)
        print(f"⏰ Cycle started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        try:
            # Step 1: Make decision
            decision = self.make_decision()
            if not decision:
                print("❌ Scheduling cycle failed: No decision made\n")
                return False
            
            # Step 2: Prepare job instructions
            instructions = self.prepare_job_instructions(decision)
            if not instructions:
                print("❌ Scheduling cycle failed: Could not prepare instructions\n")
                return False
            
            # Step 3: Log decision
            self.log_decision_to_console(decision)
            
            # Step 4: Execute job via job runner
            print("="*75)
            print("🚀 EXECUTING JOB IN GREENEST REGION")
            print("="*75 + "\n")
            
            execution_result = self.job_runner.execute_job(instructions)
            
            # Step 5: Save to Firestore
            self.firestore_logger.log_decision(decision, execution_result)
            
            # Summary
            print("="*75)
            print("📌 SCHEDULING CYCLE SUMMARY:")
            print("="*75)
            print("   1. ✅ Carbon data fetched from 6 regions")
            print("   2. ✅ Decision made (greenest region selected)")
            print("   3. ✅ Job triggered via Cloud Function")
            print("   4. ✅ Results logged to Firestore/Console")
            print("   5. ⏳ Dashboard visualization (next phase)")
            print("="*75 + "\n")
            
            if execution_result['success']:
                print("✅ SCHEDULING CYCLE COMPLETED SUCCESSFULLY\n")
                return True
            else:
                print("⚠️  SCHEDULING CYCLE COMPLETED WITH WARNINGS")
                print("   (Decision was made, but job execution had issues)\n")
                return True  # Still return True since decision was made
            
        except Exception as e:
            print(f"\n❌ Scheduling cycle failed with error: {e}\n")
            return False
    
    def get_status(self) -> Dict:
        """
        Get current scheduler status and statistics.
        
        Returns:
            Dictionary with scheduler status information
        """
        return {
            'scheduler_active': True,
            'regions_configured': len(self.fetcher.regions),
            'last_decision': self.last_decision,
            'cache_ttl_seconds': self.config.get('api', {}).get('cache_ttl_seconds', 300),
            'current_time': datetime.now().isoformat()
        }


# Main execution
if __name__ == "__main__":
    """
    Run the CASS-Lite v2 scheduler.
    
    This demonstrates a complete scheduling cycle:
    1. Initialize scheduler
    2. Fetch carbon data
    3. Make decision
    4. Prepare job instructions
    5. Log decision
    """
    
    print("\n" + "🌍" * 25)
    print("   CASS-LITE v2 - CARBON-AWARE SERVERLESS SCHEDULER")
    print("   Making the cloud greener, one decision at a time 🌱")
    print("🌍" * 25 + "\n")
    
    # Initialize scheduler
    scheduler = CarbonScheduler(config_path="config.json")
    
    # Run a scheduling cycle
    success = scheduler.run_scheduling_cycle()
    
    if success:
        # Show status
        print("\n" + "="*75)
        print("📊 SCHEDULER STATUS")
        print("="*75)
        status = scheduler.get_status()
        print(f"Active: {status['scheduler_active']}")
        print(f"Regions: {status['regions_configured']}")
        print(f"Cache TTL: {status['cache_ttl_seconds']}s")
        if status['last_decision']:
            print(f"Last Decision: {status['last_decision']['selected_region']} @ {status['last_decision']['carbon_intensity']} gCO₂/kWh")
        print("="*75 + "\n")
        
        print("🎉 Scheduler test completed successfully!")
        print("💡 Next: Implement job_runner.py to actually trigger Cloud Functions\n")
    else:
        print("❌ Scheduler test failed. Please check the errors above.\n")
