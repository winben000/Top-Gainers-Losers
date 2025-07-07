# Quick Start Guide - Daily Crypto Report Scheduler

Get your daily crypto reports sent to Telegram at 7:00 AM in 3 simple steps!

## Step 1: Setup Environment

1. **Install dependencies:**
   ```bash
   cd "Top Gainers & Losers"
   ./setup.sh
   ```

2. **Create `.env` file:**
   ```bash
   # Create .env file with your Telegram bot details
   echo "TELEGRAM_BOT_TOKEN=your_bot_token_here" > .env
   echo "TOPIC_ID=your_chat_id_here" >> .env
   ```

## Step 2: Test Telegram Integration

```bash
python3 test_telegram.py
```

This will send a test message to verify your Telegram setup is working.

## Step 3: Start Daily Scheduler

```bash
python3 daily_scheduler.py
```

The scheduler will:
- ✅ Send a startup notification
- ⏰ Run daily at 7:00 AM
- 📱 Send formatted crypto reports to Telegram
- 📁 Save data to files automatically

## Telegram Bot Setup (if you don't have one)

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow instructions
3. Copy the bot token to your `.env` file
4. Add the bot to your desired chat/channel
5. Get the chat ID (you can use [@userinfobot](https://t.me/userinfobot))

## Stop the Scheduler

Press `Ctrl+C` to stop gracefully.

## Files Created

- `crypto_data_YYYYMMDD_HHMMSS.json` - Raw data
- `daily_scheduler.log` - Scheduler logs
- `crypto_tracker.log` - Application logs

## Need Help?

- Check the logs: `tail -f daily_scheduler.log`
- Test Telegram: `python3 test_telegram.py`
- Run once: `python3 top50gainers_losers.py`

That's it! You'll receive daily crypto market updates at 7:00 AM every day! 🚀 