#!/usr/bin/env python3
"""
Test script to verify scheduler functionality
"""

import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from top50gainers_losers import run_daily_report

def test_scheduler():
    """Test the scheduler functionality"""
    print("🧪 Testing Scheduler Functionality...")
    
    # Schedule a test run in 5 seconds
    schedule.every(5).seconds.do(run_daily_report)
    
    print("⏰ Scheduled test run in 5 seconds...")
    print("🔄 Waiting for scheduled execution...")
    
    start_time = time.time()
    while time.time() - start_time < 10:  # Run for 10 seconds
        schedule.run_pending()
        time.sleep(1)
    
    print("✅ Scheduler test completed!")
    print("📱 Check your Telegram for the test message")

if __name__ == "__main__":
    test_scheduler() 