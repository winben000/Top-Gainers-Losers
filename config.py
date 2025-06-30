"""
Configuration file for Crypto Top 50 Gainers & Losers Tracker
"""

# API Keys (optional - for higher rate limits)
# Get these from the respective exchange websites
COINGECKO_API_KEY = None  # Get from https://www.coingecko.com/en/api/pricing
BINANCE_API_KEY = None    # Get from https://www.binance.com/en/my/settings/api-management
BINANCE_API_SECRET = None
BYBIT_API_KEY = None      # Get from https://www.bybit.com/en/user/settings/api-management
BYBIT_API_SECRET = None

# Data Collection Settings
TOP_COINS_COUNT = 1000    # Number of tokens to fetch for analysis (increased from 50)
VS_CURRENCY = "usd"       # Base currency (usd, eur, etc.)
REQUEST_TIMEOUT = 30      # API request timeout in seconds

# Output Settings
SAVE_TO_FILE = True       # Whether to save data to JSON file
LOG_TO_FILE = True        # Whether to log to file
LOG_LEVEL = "INFO"        # Logging level (DEBUG, INFO, WARNING, ERROR)

# Exchange Settings
ENABLE_COINGECKO = True   # Enable CoinGecko data collection
ENABLE_BINANCE = True     # Enable Binance data collection
ENABLE_BYBIT = True       # Enable Bybit data collection

# Display Settings
SHOW_TOP_COUNT = 5        # Number of top gainers/losers to show in summary
SHOW_VOLUME = True        # Show volume in summary
SHOW_MARKET_CAP = True    # Show market cap in summary (CoinGecko only) 