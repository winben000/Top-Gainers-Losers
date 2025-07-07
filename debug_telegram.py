#!/usr/bin/env python3
"""
Debug script to help identify Telegram configuration issues
"""

import asyncio
import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

async def test_telegram_config():
    """Test different Telegram configurations to find the right one"""
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    topic_id = os.getenv("TOPIC_ID")
    
    print("🔍 Debugging Telegram Configuration...")
    print(f"Bot Token: {bot_token[:10]}..." if bot_token else "❌ Bot token not found")
    print(f"Chat ID: {chat_id}")
    print(f"Topic ID: {topic_id}")
    print()
    
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in .env file")
        return
    
    # Test different chat ID formats
    test_configs = []
    
    if chat_id:
        test_configs.append(("TELEGRAM_CHAT_ID", chat_id))
    
    if topic_id:
        test_configs.append(("TOPIC_ID", topic_id))
    
    # Try without topic (just chat ID)
    if chat_id and not chat_id.startswith("-100"):
        test_configs.append(("Chat ID (without -100)", chat_id))
    
    # Try with -100 prefix for supergroups
    if chat_id and not chat_id.startswith("-100"):
        test_configs.append(("Chat ID with -100", f"-100{chat_id}"))
    
    # Try topic ID as chat ID
    if topic_id:
        test_configs.append(("Topic ID as chat", topic_id))
    
    print("🧪 Testing different configurations...")
    
    for config_name, test_chat_id in test_configs:
        print(f"\n📱 Testing {config_name}: {test_chat_id}")
        
        try:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': test_chat_id,
                'text': f"🧪 Test message from {config_name}\nChat ID: {test_chat_id}",
                'parse_mode': 'HTML'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    result = await response.json()
                    
                    if result.get('ok'):
                        print(f"✅ SUCCESS! {config_name} works!")
                        print(f"   Message ID: {result.get('result', {}).get('message_id')}")
                        return test_chat_id
                    else:
                        error_code = result.get('error_code')
                        description = result.get('description', 'Unknown error')
                        print(f"❌ Failed: {error_code} - {description}")
                        
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    print("\n❌ No working configuration found!")
    print("\n🔧 Troubleshooting steps:")
    print("1. Make sure your bot is added to the chat/channel")
    print("2. Try using @userinfobot to get your personal chat ID")
    print("3. For channels, use @getidsbot to get the channel ID")
    print("4. For supergroups, the ID should start with -100")
    print("5. Make sure the bot has permission to send messages")
    
    return None

async def get_bot_info():
    """Get information about the bot"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not bot_token:
        print("❌ Bot token not found")
        return
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                result = await response.json()
                
                if result.get('ok'):
                    bot_info = result.get('result', {})
                    print("🤖 Bot Information:")
                    print(f"   Name: {bot_info.get('first_name')}")
                    print(f"   Username: @{bot_info.get('username')}")
                    print(f"   ID: {bot_info.get('id')}")
                else:
                    print(f"❌ Failed to get bot info: {result}")
                    
    except Exception as e:
        print(f"❌ Exception getting bot info: {e}")

if __name__ == "__main__":
    print("🔍 Telegram Configuration Debug Tool")
    print("=" * 40)
    
    # Get bot info first
    asyncio.run(get_bot_info())
    print()
    
    # Test configurations
    working_chat_id = asyncio.run(test_telegram_config())
    
    if working_chat_id:
        print(f"\n🎉 SUCCESS! Use this chat ID in your .env file:")
        print(f"TELEGRAM_CHAT_ID={working_chat_id}")
        print(f"TOPIC_ID={working_chat_id}") 