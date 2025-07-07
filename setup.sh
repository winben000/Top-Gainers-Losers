#!/bin/bash

echo "🚀 Setting up Crypto Daily Report Scheduler..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Install required packages
echo "📦 Installing required packages..."
pip3 install -r requirements.txt

# Make scripts executable
chmod +x top50gainers_losers.py
chmod +x daily_scheduler.py

echo "✅ Setup completed!"
echo ""
echo "📋 Usage Instructions:"
echo "1. Run once immediately: python3 top50gainers_losers.py"
echo "2. Run scheduled daily at 7am: python3 daily_scheduler.py"
echo "3. Stop scheduler: Press Ctrl+C"
echo ""
echo "📱 Make sure your .env file contains:"
echo "   - TELEGRAM_BOT_TOKEN"
echo "   - TOPIC_ID"
echo "   - Other API keys (optional)" 