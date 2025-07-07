# Crypto Daily Report Scheduler

This project automatically fetches top 50 gainers and losers from multiple cryptocurrency exchanges (CoinGecko, Binance, Bybit) and sends daily reports to Telegram at 7:00 AM.

## Features

- 🚀 **Multi-Exchange Data**: Fetches data from CoinGecko, Binance, and Bybit
- 📊 **Top 50 Analysis**: Analyzes top 50 gainers and losers from each exchange
- 📱 **Telegram Integration**: Sends formatted reports directly to Telegram
- ⏰ **Daily Scheduling**: Automatically runs every day at 7:00 AM
- 📁 **Data Storage**: Saves data to JSON and CSV files with timestamps
- 🔄 **Error Handling**: Robust error handling with Telegram notifications

## Setup Instructions

### 1. Install Dependencies

```bash
# Run the setup script
chmod +x setup.sh
./setup.sh

# Or install manually
pip3 install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project directory with your API keys:

```env
# Required for Telegram notifications
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TOPIC_ID=your_telegram_topic_id

# Optional API keys for enhanced data access
CG_API_KEY=your_coingecko_api_key
BINANCE_API_KEY=your_binance_api_key
BINANCE_API_SECRET=your_binance_api_secret
BYBIT_API_KEY=your_bybit_api_key
BYBIT_API_SECRET=your_bybit_api_secret
```

### 3. Telegram Bot Setup

1. Create a Telegram bot using [@BotFather](https://t.me/botfather)
2. Get your bot token
3. Add the bot to your desired chat/channel
4. Get the chat ID or topic ID
5. Add these to your `.env` file

## Usage

### Run Once (Immediate Execution)

```bash
python3 top50gainers_losers.py
```

This will:
- Fetch data from all exchanges
- Save data to files
- Send a Telegram report immediately

### Run Scheduled (Daily at 7:00 AM)

```bash
python3 daily_scheduler.py
```

This will:
- Start the scheduler
- Send a startup notification to Telegram
- Run the report daily at 7:00 AM
- Send daily reports to Telegram
- Continue running until stopped (Ctrl+C)

### Stop the Scheduler

Press `Ctrl+C` to stop the scheduler gracefully. It will send a shutdown notification to Telegram.

## Output Files

The script generates several output files:

- `crypto_data_YYYYMMDD_HHMMSS.json` - Raw data in JSON format
- `daily_scheduler.log` - Scheduler logs
- `crypto_tracker.log` - Main application logs

## Telegram Message Format

The Telegram messages include:

- 📊 **Summary Statistics**: Total tokens analyzed, gainers, losers
- 🏆 **Top 10 Gainers**: From each exchange with price and volume data
- 📉 **Top 10 Losers**: From each exchange with price and volume data
- 📅 **Timestamp**: When the data was collected
- ⏰ **Next Update**: Reminder of next scheduled report

## System Requirements

- Python 3.7+
- Internet connection
- Telegram bot token and chat ID
- Optional: API keys for enhanced data access

## Troubleshooting

### Common Issues

1. **Telegram Bot Not Working**
   - Verify your bot token is correct
   - Ensure the bot is added to the chat/channel
   - Check that the topic ID is correct

2. **API Rate Limits**
   - The script includes built-in rate limiting
   - Consider adding API keys for higher limits

3. **Scheduler Not Running**
   - Check the `daily_scheduler.log` file
   - Ensure the script has proper permissions
   - Verify all dependencies are installed

### Logs

Check these log files for debugging:
- `daily_scheduler.log` - Scheduler-specific logs
- `crypto_tracker.log` - Main application logs

## Advanced Configuration

### Custom Schedule

To change the schedule time, edit `daily_scheduler.py`:

```python
# Change from 7:00 AM to 9:00 AM
schedule.every().day.at("09:00").do(run_daily_report)
```

### Multiple Times Per Day

```python
# Run at 7:00 AM and 7:00 PM
schedule.every().day.at("07:00").do(run_daily_report)
schedule.every().day.at("19:00").do(run_daily_report)
```

## Security Notes

- Keep your `.env` file secure and never commit it to version control
- API keys are optional but provide higher rate limits
- The script only reads data, no trading functionality

## Support

For issues or questions:
1. Check the log files for error messages
2. Verify your environment configuration
3. Ensure all dependencies are installed correctly 