#!/usr/bin/env python3
"""
Test script to verify Telegram integration
"""

import asyncio
import os
from dotenv import load_dotenv
from top50gainers_losers import send_telegram_message

load_dotenv()

async def test_telegram():
    """Test the Telegram message sending functionality"""
    
    # Check if environment variables are set
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    topic_id = os.getenv("TOPIC_ID")
    
    if not bot_token or not topic_id:
        print("❌ Missing Telegram configuration!")
        print("Please set TELEGRAM_BOT_TOKEN and TOPIC_ID in your .env file")
        return False

    print("✅ Telegram configuration found")
    print(f"Bot Token: {bot_token[:10]}...")
    print(f"Topic ID: {topic_id}")
    
    # Send a test message
    test_message = "🧪 <b>Telegram Integration Test</b>\n\n"
    test_message += "✅ This is a test message from your crypto tracker\n"
    test_message += "📅 If you receive this, Telegram integration is working!\n"
    test_message += "🚀 You can now run the daily scheduler"
    
    print("📱 Sending test message to Telegram...")
    
    try:
        await send_telegram_message(test_message)
        print("✅ Test message sent successfully!")
        print("📱 Check your Telegram chat for the test message")
        return True
    except Exception as e:
        print(f"❌ Failed to send test message: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Telegram Integration...")
    success = asyncio.run(test_telegram())
    
    if success:
        print("\n🎉 Telegram integration test completed successfully!")
        print("You can now run the daily scheduler with: python3 daily_scheduler.py")
    else:
        print("\n❌ Telegram integration test failed!")
        print("Please check your configuration and try again.") 