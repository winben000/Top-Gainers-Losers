# Crypto Top 50 Gainers & Losers Tracker

A comprehensive Python script that fetches the top 50 gainers and losers tokens from multiple cryptocurrency exchanges including CoinGecko, Binance, and Bybit. **Now with enhanced coverage of 1000+ tokens for more comprehensive market analysis.**

## Features

- **Multi-Exchange Support**: Fetches data from CoinGecko, Binance, and Bybit
- **Enhanced Token Coverage**: Analyzes 1000+ tokens from CoinGecko, all available USDT pairs from Binance and Bybit
- **24-Hour Timeframe**: Gets price changes over the last 24 hours
- **Comprehensive Data**: Includes price, volume, market cap, and percentage changes
- **Error Handling**: Robust error handling for API failures
- **Data Export**: Saves data to JSON files with timestamps
- **Logging**: Comprehensive logging to both file and console
- **Real-time Summary**: Displays top 5 gainers and losers from each exchange

## Token Coverage

### CoinGecko
- **1000 tokens** by market capitalization
- Includes market cap rank and comprehensive market data
- Free API tier with rate limiting

### Binance
- **All available USDT trading pairs** (typically 500+ pairs)
- Real-time 24hr ticker data
- Comprehensive volume and price change data

### Bybit
- **All available USDT spot trading pairs** (typically 500+ pairs)
- Real-time market data
- Detailed price and volume information

## Installation

1. Clone or download the script files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the script directly:

```bash
python top50gainers_losers.py
```

### With API Keys (Optional)

For better rate limits and access, you can add API keys:

```python
# In the main() function, uncomment and add your API keys:
aggregator = CryptoDataAggregator(
    coingecko_api_key="your_coingecko_api_key_here",
    binance_api_key="your_binance_api_key_here",
    binance_api_secret="your_binance_api_secret_here",
    bybit_api_key="your_bybit_api_key_here",
    bybit_api_secret="your_bybit_api_secret_here"
)
```

## Output

The script provides:

1. **Console Output**: Real-time summary of top gainers and losers
2. **JSON File**: Complete data saved to `crypto_data_YYYYMMDD_HHMMSS.json`
3. **Log File**: Detailed logs saved to `crypto_tracker.log`

### Sample Output

```
================================================================================
CRYPTO TOP 50 GAINERS & LOSERS SUMMARY
================================================================================

COINGECKO EXCHANGE:
----------------------------------------
✅ Success - Data fetched at 2025-06-28T00:42:19.079483
📊 Top Gainers: 45 tokens
📉 Top Losers: 50 tokens

🏆 TOP 5 GAINERS:
  1. SEI (Sei)
     Price: $0.281206
     Change: +8.46%
     Volume: $706,910,583
  2. RENDER (Render)
     Price: $3.140000
     Change: +5.35%
     Volume: $100,766,923

BINANCE EXCHANGE:
----------------------------------------
✅ Success - Data fetched at 2025-06-28T00:42:20.131046
📊 Top Gainers: 50 tokens
📉 Top Losers: 50 tokens
Found 407 USDT trading pairs on Binance
Processed 593 USDT pairs with valid data

🏆 TOP 5 GAINERS:
  1. HIFI (HIFI)
     Price: $0.128300
     Change: +33.37%
     Volume: $29,238,681
```

## Data Structure

### TokenData
```python
@dataclass
class TokenData:
    symbol: str              # Token symbol (e.g., "BTC")
    name: str                # Token name (e.g., "Bitcoin")
    price: float             # Current price in USD
    price_change_24h: float  # Absolute price change in 24h
    price_change_percentage_24h: float  # Percentage change in 24h
    volume_24h: float        # 24h trading volume in USD
    market_cap: Optional[float] = None  # Market capitalization
    rank: Optional[int] = None          # Market cap rank
    exchange: str = ""       # Source exchange
    timestamp: str = ""      # Data timestamp
```

### ExchangeData
```python
@dataclass
class ExchangeData:
    exchange: str                    # Exchange name
    gainers: List[TokenData]        # Top 50 gainers
    losers: List[TokenData]         # Top 50 losers
    timestamp: str                  # Data timestamp
    success: bool                   # API call success status
    error: Optional[str] = None     # Error message if failed
```

## API Endpoints Used

### CoinGecko
- **Endpoint**: `/coins/markets`
- **Parameters**: `vs_currency=usd`, `per_page=1000`, `order=market_cap_desc`
- **Coverage**: Top 1000 tokens by market cap
- **Rate Limit**: Free tier available, Pro API recommended for production

### Binance
- **Endpoint**: `/api/v3/ticker/24hr`
- **Coverage**: All available USDT trading pairs
- **Rate Limit**: 1200 requests per minute
- **Authentication**: Optional (higher rate limits with API key)

### Bybit
- **Endpoint**: `/v5/market/tickers`
- **Parameters**: `category=spot`
- **Coverage**: All available USDT spot trading pairs
- **Rate Limit**: 120 requests per second
- **Authentication**: Optional (higher rate limits with API key)

## Enhanced Coverage Benefits

### Before (Limited Coverage)
- CoinGecko: ~100 tokens
- Binance: Limited USDT pairs
- Bybit: Limited spot pairs

### After (Enhanced Coverage)
- **CoinGecko**: 1000 tokens by market cap
- **Binance**: All 500+ USDT trading pairs
- **Bybit**: All 500+ USDT spot trading pairs
- **Total Coverage**: 2000+ unique tokens across all exchanges

This ensures you get the **true top 50 gainers and losers** from a much larger pool of tokens, providing more accurate market insights.

## Error Handling

The script includes comprehensive error handling:

- **Network Timeouts**: 30-second timeout for all API calls
- **API Errors**: Graceful handling of API errors with detailed logging
- **Data Validation**: Skips invalid data entries
- **Rate Limiting**: Respects exchange rate limits

## Logging

Logs are written to both:
- **Console**: Real-time status updates
- **File**: `crypto_tracker.log` for detailed debugging

## Customization

### Adding More Exchanges

To add support for additional exchanges:

1. Create a new API class following the pattern of existing ones
2. Implement the `get_24hr_ticker()` method
3. Add the exchange to the `CryptoDataAggregator` class

### Modifying Data Fields

Edit the `TokenData` dataclass to add or remove fields as needed.

### Changing Timeframes

Currently set to 24-hour timeframe. Modify the API calls to support different timeframes.

## Dependencies

- `requests`: HTTP library for API calls
- `python-dateutil`: Date and time utilities
- Standard library: `json`, `logging`, `dataclasses`, `typing`, `datetime`

## License

This script is provided as-is for educational and research purposes.

## Disclaimer

This tool is for informational purposes only. Cryptocurrency trading involves significant risk. Always do your own research and consider consulting with financial advisors before making investment decisions.

## Support

For issues or questions:
1. Check the log file for detailed error messages
2. Verify your internet connection
3. Ensure all dependencies are installed correctly
4. Check if the exchanges' APIs are accessible 