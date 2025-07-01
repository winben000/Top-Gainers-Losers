import asyncio
import ccxt.pro as ccxt
import os
import json
import logging
from datetime import datetime
import pandas as pd
import time
import subprocess
import sys
from dotenv import load_dotenv
import requests
import aiohttp

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID =  os.getenv("TELEGRAM_CHAT_ID")
TOPIC_ID = os.getenv("TOPIC_ID")

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Config
CONFIG_PATH = "gateio_more.json"  # Change as needed
CSV_FILE = "auto_trades.csv"      # Output CSV file
PLOT_SCRIPT = "plot.py"           # Path to plot.py
PLOT_PREFIX = "AUTO"
ANALYZE_INTERVAL = 15 * 60         # 15 minutes in seconds

# --- Telegram send function ---
async def send_telegram_photo(photo_path, caption=None):
    """
    Send a photo to Telegram using the bot API.
    Uses aiohttp for async HTTP requests.
    Includes message_thread_id if TOPIC_ID is set (for forum topics).
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error("Telegram credentials not set in environment variables.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption or "", "parse_mode": "HTML"}
    if TOPIC_ID:
        data["message_thread_id"] = TOPIC_ID
    try:
        with open(photo_path, "rb") as photo:
            form = aiohttp.FormData()
            for k, v in data.items():
                form.add_field(k, str(v))
            form.add_field('photo', photo, filename=os.path.basename(photo_path), content_type='image/png')
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=form) as response:
                    result = await response.json()
                    if response.status != 200:
                        logger.error(f"Telegram API error: {result}")
                    else:
                        logger.info(f"Telegram photo sent successfully: {photo_path}")
    except Exception as e:
        logger.error(f"Error sending Telegram photo: {e}")

# --- Streaming trades ---
async def stream_trades(exchange_id, symbol):
    logger.info(f"Starting trade stream for {exchange_id} {symbol}")
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({"enableRateLimit": True})
    header_written = os.path.exists(CSV_FILE)
    while True:
        try:
            trades = await exchange.watch_trades(symbol)
            if trades:
                df = pd.DataFrame(trades)
                df['amount'] = df['amount'].astype(float)
                df['price'] = df['price'].astype(float)
                # Add category column
                def categorize(amount):
                    if amount < 100: return 'small'
                    elif amount < 1000: return 'medium'
                    else: return 'large'
                df['category'] = df['amount'].apply(categorize)
                # Append to CSV
                df.to_csv(CSV_FILE, index=False, mode='a' if header_written else 'w', header=not header_written)
                header_written = True
                logger.info(f"Appended {len(df)} trades to {CSV_FILE}")
        except Exception as e:
            logger.error(f"Stream error: {e}")
            await asyncio.sleep(10)

# --- Scheduled analysis and reporting ---
async def analyze_and_report():
    while True:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            prefix = f"{PLOT_PREFIX}_{timestamp}"
            # Call plot.py to save plots
            cmd = [sys.executable, PLOT_SCRIPT, CSV_FILE, "--datetime", "datetime", "--save-prefix", prefix]
            logger.info(f"Running: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            # Send plots to Telegram
            for suffix in ["TRADEPRICEOVERTIME.png", "NOTIONALOVERTIME.png"]:
                plot_path = f"{prefix}_{suffix}"
                if os.path.exists(plot_path):
                    await send_telegram_photo(plot_path, caption=f"{suffix} {timestamp}")
                else:
                    logger.warning(f"Plot not found: {plot_path}")
        except Exception as e:
            logger.error(f"Analysis/report error: {e}")
        logger.info(f"Sleeping {ANALYZE_INTERVAL//60} minutes before next analysis...")
        await asyncio.sleep(ANALYZE_INTERVAL)

# --- Main entry point ---
async def main():
    # Load config
    try:
        with open(CONFIG_PATH) as f:
            config = json.load(f)
        exchange_id = config.get("exchange", "gateio")
        symbol = config.get("symbol", "MORE/USDT")
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return
    # Start streaming and reporting concurrently
    await asyncio.gather(
        stream_trades(exchange_id, symbol),
        analyze_and_report()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...") 