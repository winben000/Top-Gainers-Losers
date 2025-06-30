#!/usr/bin/env python3
"""
Daily Crypto Tracker Runner
This script can be scheduled to run daily using cron or other schedulers
"""

import os
import sys
from datetime import datetime
from top50gainers_losers import CryptoDataAggregator

def run_daily_tracker():
    """Run the crypto tracker and save data with daily timestamp"""
    
    # Create daily data directory if it doesn't exist
    daily_dir = "daily_data"
    if not os.path.exists(daily_dir):
        os.makedirs(daily_dir)
    
    # Generate filename with date
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{daily_dir}/crypto_data_{today}.json"
    
    print(f"🔄 Running daily crypto tracker for {today}...")
    
    try:
        # Initialize the aggregator
        aggregator = CryptoDataAggregator()
        
        # Get data from all exchanges
        data = aggregator.get_all_exchange_data()
        
        # Save data to daily file
        aggregator.save_data_to_file(data, filename)
        
        # Print summary
        aggregator.print_summary(data)
        
        print(f"✅ Daily data collection completed for {today}")
        print(f"📁 Data saved to {filename}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in daily tracker: {e}")
        return False

if __name__ == "__main__":
    success = run_daily_tracker()
    sys.exit(0 if success else 1) 