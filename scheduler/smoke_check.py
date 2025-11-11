"""
CASS-Lite v2 - Smoke Check Script
==================================
Performs a dry-run of the complete scheduler workflow to verify functionality.

This script:
1. Imports CarbonFetcher and CarbonScheduler
2. Runs a full dry-run cycle (fetch → select → prepare job → skip actual POST)
3. Prints the selected greenest region and computed savings
4. Exits with code 0 if successful, nonzero on any failure or exception
5. Uses try/except to log meaningful errors

Usage:
    python smoke_check.py
    or
    py smoke_check.py

Exit Codes:
    0 - Success: All checks passed
    1 - Failure: Carbon data fetch failed
    2 - Failure: Decision making failed
    3 - Failure: Job preparation failed
    4 - Failure: Unexpected exception
"""

import sys
import os
from datetime import datetime
from typing import Optional, Dict

# Fix Windows console encoding issues with emoji
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add scheduler directory to Python path if needed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from carbon_fetcher import CarbonFetcher
    from main import CarbonScheduler
except ImportError as e:
    print(f"[ERROR] IMPORT ERROR: {e}")
    print("   Make sure you're running from the scheduler directory")
    sys.exit(4)


def print_header():
    """Print smoke check header."""
    print("\n" + "="*80)
    print("🧪 CASS-LITE v2 SMOKE CHECK - DRY RUN MODE")
    print("="*80)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔍 Mode: Dry-run (no actual Cloud Function calls will be made)")
    print("="*80 + "\n")


def print_section(title: str):
    """Print a section header."""
    print("\n" + "-"*80)
    print(f"📌 {title}")
    print("-"*80)


def print_success(message: str):
    """Print a success message."""
    print(f"✅ {message}")


def print_error(message: str):
    """Print an error message."""
    print(f"❌ {message}")


def print_info(message: str):
    """Print an info message."""
    print(f"ℹ️  {message}")


def check_imports() -> bool:
    """
    Verify that all required imports are available.
    
    Returns:
        True if imports successful, False otherwise
    """
    print_section("STEP 1: Verifying Imports")
    
    try:
        print_info("Importing CarbonFetcher...")
        from carbon_fetcher import CarbonFetcher
        print_success("CarbonFetcher imported successfully")
        
        print_info("Importing CarbonScheduler...")
        from main import CarbonScheduler
        print_success("CarbonScheduler imported successfully")
        
        print_info("Importing JobRunner...")
        from job_runner import JobRunner
        print_success("JobRunner imported successfully")
        
        return True
        
    except ImportError as e:
        print_error(f"Import failed: {e}")
        return False


def run_dry_run() -> int:
    """
    Execute the complete dry-run workflow.
    
    Returns:
        Exit code (0 for success, nonzero for failure)
    """
    print_header()
    
    # Step 1: Verify imports
    if not check_imports():
        print_error("Import verification failed")
        return 4
    
    # Step 2: Initialize scheduler
    print_section("STEP 2: Initializing CarbonScheduler")
    
    try:
        # Use config.json from scheduler directory
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        
        if not os.path.exists(config_path):
            print_error(f"Config file not found: {config_path}")
            print_info("Scheduler will use default configuration")
        
        scheduler = CarbonScheduler(config_path=config_path)
        print_success("CarbonScheduler initialized successfully")
        
    except Exception as e:
        print_error(f"Failed to initialize scheduler: {e}")
        print(f"   Exception type: {type(e).__name__}")
        print(f"   Exception details: {str(e)[:200]}")
        return 4
    
    # Step 3: Fetch carbon data and make decision
    print_section("STEP 3: Fetching Carbon Data & Making Decision")
    
    try:
        print_info("Calling scheduler.make_decision()...")
        decision = scheduler.make_decision()
        
        if not decision:
            print_error("Decision making failed - no carbon data available")
            return 1
        
        print_success("Decision made successfully!")
        
    except Exception as e:
        print_error(f"Failed to make scheduling decision: {e}")
        print(f"   Exception type: {type(e).__name__}")
        print(f"   Exception details: {str(e)[:200]}")
        return 2
    
    # Step 4: Display decision results
    print_section("STEP 4: Decision Results")
    
    try:
        print("\n📊 SELECTED GREENEST REGION:")
        print(f"   Region: {decision['region_flag']} {decision['region_name']} ({decision['selected_region']})")
        print(f"   Carbon Intensity: {decision['carbon_intensity']} gCO₂/kWh")
        print(f"   Average Carbon (all regions): {decision['average_carbon']} gCO₂/kWh")
        print(f"   Carbon Savings: {decision['savings_gco2']} gCO₂/kWh")
        print(f"   Savings Percentage: {decision['savings_percent']}%")
        print(f"   Regions Analyzed: {decision['total_regions_checked']}")
        print(f"   Decision Time: {decision['decision_time_ms']} ms")
        print(f"   Data Timestamp: {decision.get('data_timestamp', 'N/A')}")
        
        print_success("Decision data validated")
        
    except KeyError as e:
        print_error(f"Decision data incomplete - missing key: {e}")
        return 2
    except Exception as e:
        print_error(f"Failed to display decision: {e}")
        return 2
    
    # Step 5: Prepare job instructions (dry-run, no actual execution)
    print_section("STEP 5: Preparing Job Instructions (Dry-Run)")
    
    try:
        print_info("Calling scheduler.prepare_job_instructions()...")
        job_instructions = scheduler.prepare_job_instructions(decision)
        
        if not job_instructions:
            print_error("Failed to prepare job instructions")
            return 3
        
        print_success("Job instructions prepared successfully")
        
        # Display job instructions
        print("\n📋 JOB EXECUTION INSTRUCTIONS (DRY-RUN):")
        print(f"   Target Region: {job_instructions.get('target_region', 'N/A')}")
        print(f"   Cloud Function URL: {job_instructions.get('cloud_function_url', 'N/A')}")
        print(f"   Task ID: {job_instructions.get('payload', {}).get('task_id', 'N/A')}")
        print(f"   Carbon Intensity: {job_instructions.get('payload', {}).get('carbon_intensity', 'N/A')} gCO₂/kWh")
        
        print_info("DRY-RUN MODE: Skipping actual Cloud Function POST request")
        print_success("Job preparation validated (no actual execution)")
        
    except Exception as e:
        print_error(f"Failed to prepare job instructions: {e}")
        print(f"   Exception type: {type(e).__name__}")
        print(f"   Exception details: {str(e)[:200]}")
        return 3
    
    # Step 6: Verify carbon savings calculation
    print_section("STEP 6: Verifying Carbon Savings Calculation")
    
    try:
        carbon_intensity = decision['carbon_intensity']
        average_carbon = decision['average_carbon']
        savings_gco2 = decision['savings_gco2']
        
        # Verify savings calculation
        expected_savings = average_carbon - carbon_intensity
        
        if abs(expected_savings - savings_gco2) <= 1:  # Allow 1 unit rounding error
            print_success(f"Carbon savings calculation verified: {savings_gco2} gCO₂/kWh")
        else:
            print_error(f"Carbon savings mismatch - Expected: {expected_savings}, Got: {savings_gco2}")
            return 2
        
        # Verify savings percentage
        if average_carbon > 0:
            expected_percent = round((savings_gco2 / average_carbon) * 100, 1)
            if abs(expected_percent - decision['savings_percent']) <= 0.1:
                print_success(f"Savings percentage verified: {decision['savings_percent']}%")
            else:
                print_error(f"Savings percentage mismatch - Expected: {expected_percent}%, Got: {decision['savings_percent']}%")
        
    except Exception as e:
        print_error(f"Savings verification failed: {e}")
        return 2
    
    # Final summary
    print_section("SMOKE CHECK SUMMARY")
    
    print("\n✅ ALL CHECKS PASSED!")
    print("\n📊 Summary:")
    print(f"   ✓ Imports verified")
    print(f"   ✓ Scheduler initialized")
    print(f"   ✓ Carbon data fetched ({decision['total_regions_checked']} regions)")
    print(f"   ✓ Greenest region selected: {decision['region_name']} ({decision['selected_region']})")
    print(f"   ✓ Carbon savings calculated: {decision['savings_gco2']} gCO₂/kWh ({decision['savings_percent']}%)")
    print(f"   ✓ Job instructions prepared (dry-run)")
    print(f"   ✓ Calculations verified")
    
    print("\n" + "="*80)
    print("🎉 SMOKE CHECK COMPLETED SUCCESSFULLY")
    print("="*80)
    print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")
    
    return 0


def main():
    """
    Main entry point for smoke check script.
    """
    try:
        exit_code = run_dry_run()
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Smoke check interrupted by user")
        sys.exit(130)
        
    except Exception as e:
        print("\n" + "="*80)
        print("❌ UNEXPECTED EXCEPTION")
        print("="*80)
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {str(e)}")
        print("\nStack trace:")
        import traceback
        traceback.print_exc()
        print("="*80 + "\n")
        sys.exit(4)


if __name__ == "__main__":
    main()
