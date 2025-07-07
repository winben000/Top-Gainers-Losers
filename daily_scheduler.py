#!/usr/bin/env python3
"""
Daily Crypto Report Scheduler
Runs the crypto tracker every day at 7:00 AM and sends results to Telegram
"""

import schedule
import time
import logging
from datetime import datetime
import sys
import os

# Add the current directory to Python path to import the main module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from top50gainers_losers import run_daily_report, send_telegram_message
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('daily_scheduler.log'),
        logging.StreamHandler()
    ]
)

def send_startup_message():
    """Send a startup message to Telegram"""
    startup_message = f"🚀 <b>Crypto Daily Report Scheduler Started</b>\n\n"
    startup_message += f"⏰ Scheduled to run daily at 7:00 AM\n"
    startup_message += f"📅 Started on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    startup_message += f"✅ Scheduler is running and monitoring..."
    
    try:
        asyncio.run(send_telegram_message(startup_message))
        logging.info("Startup message sent to Telegram")
    except Exception as e:
        logging.error(f"Failed to send startup message: {e}")

def send_shutdown_message():
    """Send a shutdown message to Telegram"""
    shutdown_message = f"🛑 <b>Crypto Daily Report Scheduler Stopped</b>\n\n"
    shutdown_message += f"📅 Stopped on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    shutdown_message += f"⚠️ Daily reports will no longer be sent automatically"
    
    try:
        asyncio.run(send_telegram_message(shutdown_message))
        logging.info("Shutdown message sent to Telegram")
    except Exception as e:
        logging.error(f"Failed to send shutdown message: {e}")

def main():
    """Main function to run the scheduler"""
    print("🚀 Starting Crypto Daily Report Scheduler...")
    print("⏰ Reports will be sent daily at 7:00 AM")
    print("📱 Telegram notifications enabled")
    print("🔄 Scheduler is running... (Press Ctrl+C to stop)")
    
    # Send startup message
    send_startup_message()
    
    # Schedule the daily report
    schedule.every().day.at("07:00").do(run_daily_report)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        print("\n⏹️  Shutting down scheduler...")
        send_shutdown_message()
        print("✅ Scheduler stopped gracefully")
    except Exception as e:
        error_msg = f"❌ Scheduler error: {e}"
        logging.error(error_msg)
        print(error_msg)
        
        # Send error message to Telegram
        try:
            asyncio.run(send_telegram_message(f"❌ <b>Scheduler Error</b>\n\n{error_msg}"))
        except:
            pass

if __name__ == "__main__":
    main() 