#!/usr/bin/env python3
"""
Top 50 Gainers and Losers Token Tracker
Fetches data from CoinGecko, Binance, and Bybit exchanges
"""

import requests
import time
import json
import csv
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import logging
from dotenv import load_dotenv
import os

load_dotenv()
cg_api_key = os.getenv("CG_API_KEY")
binance_api_key = os.getenv("BINANCE_API_KEY")
binance_api_secret = os.getenv("BINANCE_API_SECRET")
bybit_api_key = os.getenv("BYBIT_API_KEY")
bybit_api_secret = os.getenv("BYBIT_API_SECRET")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crypto_tracker.log'),
        logging.StreamHandler()
    ]
)

@dataclass
class TokenData:
    """Data structure for token information"""
    symbol: str
    name: str
    price: float
    price_change_24h: float
    price_change_percentage_24h: float
    volume_24h: float
    market_cap: Optional[float] = None
    rank: Optional[int] = None
    exchange: str = ""
    timestamp: str = ""

@dataclass
class ExchangeData:
    """Data structure for exchange results"""
    exchange: str
    gainers: List[TokenData]
    losers: List[TokenData]
    timestamp: str
    success: bool
    error: Optional[str] = None

class CoinGeckoAPI:
    """CoinGecko API integration"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.pro_url = "https://pro-api.coingecko.com/api/v3"
        self.api_key = api_key
        self.headers = {}
        
        if api_key:
            self.headers["x_cg_pro_api_key"] = api_key
            self.base_url = self.pro_url
    
    def get_top_gainers_losers(self, vs_currency: str = "usd", top_coins: int = 1000) -> ExchangeData:
        """Get top 50 gainers and losers from CoinGecko, using pagination for up to 1000 tokens"""
        try:
            all_data = []
            per_page = 250
            pages = (top_coins // per_page) + (1 if top_coins % per_page else 0)
            for page in range(1, pages + 1):
                url = f"{self.base_url}/coins/markets"
                params = {
                    "vs_currency": vs_currency,
                    "order": "market_cap_desc",
                    "per_page": per_page,
                    "page": page,
                    "sparkline": False,
                    "price_change_percentage": "24h"
                }
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                all_data.extend(data)
                if len(all_data) >= top_coins or len(data) < per_page:
                    break
            logging.info(f"CoinGecko: Fetched {len(all_data)} tokens for analysis (pagination)")
            # Sort by 24h price change percentage
            all_data.sort(key=lambda x: x.get("price_change_percentage_24h", 0) or 0, reverse=True)
            gainers = []
            losers = []
            # Process gainers (positive price changes)
            for token in all_data:
                if token.get("price_change_percentage_24h", 0) > 0:
                    gainers.append(TokenData(
                        symbol=token.get("symbol", "").upper(),
                        name=token.get("name", ""),
                        price=token.get("current_price", 0),
                        price_change_24h=token.get("price_change_24h", 0),
                        price_change_percentage_24h=token.get("price_change_percentage_24h", 0),
                        volume_24h=token.get("total_volume", 0),
                        market_cap=token.get("market_cap", 0),
                        rank=token.get("market_cap_rank"),
                        exchange="CoinGecko",
                        timestamp=datetime.now().isoformat()
                    ))
                    if len(gainers) >= 50:
                        break
            # Process losers (negative price changes)
            for token in reversed(all_data):
                if token.get("price_change_percentage_24h", 0) < 0:
                    losers.append(TokenData(
                        symbol=token.get("symbol", "").upper(),
                        name=token.get("name", ""),
                        price=token.get("current_price", 0),
                        price_change_24h=token.get("price_change_24h", 0),
                        price_change_percentage_24h=token.get("price_change_percentage_24h", 0),
                        volume_24h=token.get("total_volume", 0),
                        market_cap=token.get("market_cap", 0),
                        rank=token.get("market_cap_rank"),
                        exchange="CoinGecko",
                        timestamp=datetime.now().isoformat()
                    ))
                    if len(losers) >= 50:
                        break
            logging.info(f"CoinGecko: Found {len(gainers)} gainers and {len(losers)} losers")
            return ExchangeData(
                exchange="CoinGecko",
                gainers=gainers,
                losers=losers,
                timestamp=datetime.now().isoformat(),
                success=True
            )
        except Exception as e:
            logging.error(f"CoinGecko API error: {e}")
            return ExchangeData(
                exchange="CoinGecko",
                gainers=[],
                losers=[],
                timestamp=datetime.now().isoformat(),
                success=False,
                error=str(e)
            )

class BinanceAPI:
    """Binance API integration"""
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        self.base_url = "https://api.binance.com/api/v3"
        self.api_key = api_key
        self.api_secret = api_secret
    
    def get_24hr_ticker(self) -> ExchangeData:
        """Get 24hr ticker statistics for all symbols"""
        try:
            # Set up authentication headers if API key is provided
            headers = {}
            if self.api_key:
                headers["X-MBX-APIKEY"] = self.api_key
            
            # First get all exchange info to see all available symbols
            info_url = f"{self.base_url}/exchangeInfo"
            info_response = requests.get(info_url, headers=headers, timeout=30)
            info_response.raise_for_status()
            exchange_info = info_response.json()
            
            # Get all USDT symbols
            usdt_symbols = []
            for symbol_info in exchange_info.get("symbols", []):
                if (symbol_info["status"] == "TRADING" and 
                    symbol_info["quoteAsset"] == "USDT" and
                    symbol_info["isSpotTradingAllowed"]):
                    usdt_symbols.append(symbol_info["symbol"])
            
            logging.info(f"Found {len(usdt_symbols)} USDT trading pairs on Binance")
            
            # Get 24hr ticker for all symbols
            url = f"{self.base_url}/ticker/24hr"
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Filter USDT pairs and calculate percentage changes
            usdt_pairs = []
            for ticker in data:
                if ticker["symbol"].endswith("USDT"):
                    try:
                        price = float(ticker["lastPrice"])
                        price_change = float(ticker["priceChange"])
                        price_change_percent = float(ticker["priceChangePercent"])
                        volume = float(ticker["volume"])
                        quote_volume = float(ticker["quoteVolume"])
                        
                        usdt_pairs.append({
                            "symbol": ticker["symbol"].replace("USDT", ""),
                            "name": ticker["symbol"].replace("USDT", ""),
                            "price": price,
                            "price_change_24h": price_change,
                            "price_change_percentage_24h": price_change_percent,
                            "volume_24h": quote_volume,
                            "base_volume": volume
                        })
                    except (ValueError, KeyError):
                        continue
            
            logging.info(f"Processed {len(usdt_pairs)} USDT pairs with valid data")
            
            # Sort by percentage change
            usdt_pairs.sort(key=lambda x: x["price_change_percentage_24h"], reverse=True)
            
            gainers = []
            losers = []
            
            # Top 50 gainers
            for token in usdt_pairs[:50]:
                gainers.append(TokenData(
                    symbol=token["symbol"],
                    name=token["name"],
                    price=token["price"],
                    price_change_24h=token["price_change_24h"],
                    price_change_percentage_24h=token["price_change_percentage_24h"],
                    volume_24h=token["volume_24h"],
                    exchange="Binance",
                    timestamp=datetime.now().isoformat()
                ))
            
            # Top 50 losers
            for token in usdt_pairs[-50:]:
                losers.append(TokenData(
                    symbol=token["symbol"],
                    name=token["name"],
                    price=token["price"],
                    price_change_24h=token["price_change_24h"],
                    price_change_percentage_24h=token["price_change_percentage_24h"],
                    volume_24h=token["volume_24h"],
                    exchange="Binance",
                    timestamp=datetime.now().isoformat()
                ))
            
            return ExchangeData(
                exchange="Binance",
                gainers=gainers,
                losers=losers,
                timestamp=datetime.now().isoformat(),
                success=True
            )
            
        except Exception as e:
            logging.error(f"Binance API error: {e}")
            return ExchangeData(
                exchange="Binance",
                gainers=[],
                losers=[],
                timestamp=datetime.now().isoformat(),
                success=False,
                error=str(e)
            )

class BybitAPI:
    """Bybit API integration"""
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        self.base_url = "https://api.bybit.com/v5"
        self.api_key = api_key
        self.api_secret = api_secret
    
    def get_24hr_ticker(self) -> ExchangeData:
        """Get 24hr ticker statistics for all symbols"""
        try:
            # Set up authentication headers if API key is provided
            headers = {}
            if self.api_key:
                headers["X-BAPI-API-KEY"] = self.api_key
                # Note: For read-only operations, we don't need to sign the request
                # For more complex operations, we would need to implement HMAC signing
            
            # Get all available symbols first
            symbols_url = f"{self.base_url}/market/instruments-info"
            symbols_params = {"category": "spot"}
            symbols_response = requests.get(symbols_url, params=symbols_params, headers=headers, timeout=30)
            symbols_response.raise_for_status()
            symbols_data = symbols_response.json()
            
            if symbols_data.get("retCode") != 0:
                raise Exception(f"Bybit symbols API error: {symbols_data.get('retMsg', 'Unknown error')}")
            
            # Get all USDT symbols
            usdt_symbols = []
            for symbol_info in symbols_data.get("result", {}).get("list", []):
                if (symbol_info["status"] == "Trading" and 
                    symbol_info["quoteCoin"] == "USDT"):
                    usdt_symbols.append(symbol_info["symbol"])
            
            logging.info(f"Found {len(usdt_symbols)} USDT trading pairs on Bybit")
            
            # Get 24hr ticker for all symbols
            url = f"{self.base_url}/market/tickers"
            params = {"category": "spot"}
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data.get("retCode") != 0:
                raise Exception(f"Bybit API error: {data.get('retMsg', 'Unknown error')}")
            
            tickers = data.get("result", {}).get("list", [])
            
            # Filter USDT pairs and calculate percentage changes
            usdt_pairs = []
            for ticker in tickers:
                if ticker["symbol"].endswith("USDT"):
                    try:
                        price = float(ticker["lastPrice"])
                        price_change = float(ticker["price24hPcnt"]) * price  # Convert percentage to absolute
                        price_change_percent = float(ticker["price24hPcnt"]) * 100  # Convert to percentage
                        volume = float(ticker["volume24h"])
                        turnover = float(ticker["turnover24h"])
                        
                        usdt_pairs.append({
                            "symbol": ticker["symbol"].replace("USDT", ""),
                            "name": ticker["symbol"].replace("USDT", ""),
                            "price": price,
                            "price_change_24h": price_change,
                            "price_change_percentage_24h": price_change_percent,
                            "volume_24h": turnover,
                            "base_volume": volume
                        })
                    except (ValueError, KeyError):
                        continue
            
            logging.info(f"Processed {len(usdt_pairs)} USDT pairs with valid data")
            
            # Sort by percentage change
            usdt_pairs.sort(key=lambda x: x["price_change_percentage_24h"], reverse=True)
            
            gainers = []
            losers = []
            
            # Top 50 gainers
            for token in usdt_pairs[:50]:
                gainers.append(TokenData(
                    symbol=token["symbol"],
                    name=token["name"],
                    price=token["price"],
                    price_change_24h=token["price_change_24h"],
                    price_change_percentage_24h=token["price_change_percentage_24h"],
                    volume_24h=token["volume_24h"],
                    exchange="Bybit",
                    timestamp=datetime.now().isoformat()
                ))
            
            # Top 50 losers
            for token in usdt_pairs[-50:]:
                losers.append(TokenData(
                    symbol=token["symbol"],
                    name=token["name"],
                    price=token["price"],
                    price_change_24h=token["price_change_24h"],
                    price_change_percentage_24h=token["price_change_percentage_24h"],
                    volume_24h=token["volume_24h"],
                    exchange="Bybit",
                    timestamp=datetime.now().isoformat()
                ))
            
            return ExchangeData(
                exchange="Bybit",
                gainers=gainers,
                losers=losers,
                timestamp=datetime.now().isoformat(),
                success=True
            )
            
        except Exception as e:
            logging.error(f"Bybit API error: {e}")
            return ExchangeData(
                exchange="Bybit",
                gainers=[],
                losers=[],
                timestamp=datetime.now().isoformat(),
                success=False,
                error=str(e)
            )

class CryptoDataAggregator:
    """Main class to aggregate data from multiple exchanges"""
    
    def __init__(self, coingecko_api_key: Optional[str] = None, 
                 binance_api_key: Optional[str] = None, 
                 binance_api_secret: Optional[str] = None,
                 bybit_api_key: Optional[str] = None,
                 bybit_api_secret: Optional[str] = None):
        
        self.coingecko = CoinGeckoAPI(coingecko_api_key)
        self.binance = BinanceAPI(binance_api_key, binance_api_secret)
        self.bybit = BybitAPI(bybit_api_key, bybit_api_secret)
    
    def get_all_exchange_data(self) -> Dict[str, ExchangeData]:
        """Get data from all exchanges"""
        results = {}
        
        # Get CoinGecko data
        logging.info("Fetching data from CoinGecko...")
        results["coingecko"] = self.coingecko.get_top_gainers_losers(top_coins=1000)
        
        # Get Binance data
        logging.info("Fetching data from Binance...")
        results["binance"] = self.binance.get_24hr_ticker()
        
        # Get Bybit data
        logging.info("Fetching data from Bybit...")
        results["bybit"] = self.bybit.get_24hr_ticker()
        
        return results
    
    def save_data_to_file(self, data: Dict[str, ExchangeData], filename: Optional[str] = None):
        """Save data to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crypto_data_{timestamp}.json"
        
        # Convert dataclasses to dictionaries
        serializable_data = {}
        for exchange, exchange_data in data.items():
            serializable_data[exchange] = {
                "exchange": exchange_data.exchange,
                "timestamp": exchange_data.timestamp,
                "success": exchange_data.success,
                "error": exchange_data.error,
                "gainers": [asdict(token) for token in exchange_data.gainers],
                "losers": [asdict(token) for token in exchange_data.losers]
            }
        
        with open(filename, 'w') as f:
            json.dump(serializable_data, f, indent=2)
        
        logging.info(f"Data saved to {filename}")
    
    def print_summary(self, data: Dict[str, ExchangeData]):
        """Print a summary of the data"""
        print("\n" + "="*80)
        print("CRYPTO TOP 50 GAINERS & LOSERS SUMMARY")
        print("="*80)
        print("🎯 Enhanced Coverage: 1000+ tokens analyzed for comprehensive market insights")
        print("="*80)
        
        total_gainers = 0
        total_losers = 0
        
        for exchange_name, exchange_data in data.items():
            print(f"\n{exchange_name.upper()} EXCHANGE:")
            print("-" * 40)
            
            if not exchange_data.success:
                print(f"❌ Error: {exchange_data.error}")
                continue
            
            gainers = exchange_data.gainers
            losers = exchange_data.losers
            total_gainers += len(gainers)
            total_losers += len(losers)
            
            print(f"✅ Success - Data fetched at {exchange_data.timestamp}")
            print(f"📊 Top Gainers: {len(gainers)} tokens")
            print(f"📉 Top Losers: {len(losers)} tokens")
            
            if gainers:
                print(f"\n🏆 TOP 50 GAINERS:")
                for i, token in enumerate(gainers, 1):
                    print(f"  {i:2d}. {token.symbol:<8} ({token.name:<20}) ${token.price:<10.6f} {token.price_change_percentage_24h:+.2f}% ${token.volume_24h:,.0f}")
            
            if losers:
                print(f"\n📉 TOP 50 LOSERS:")
                for i, token in enumerate(losers, 1):
                    print(f"  {i:2d}. {token.symbol:<8} ({token.name:<20}) ${token.price:<10.6f} {token.price_change_percentage_24h:+.2f}% ${token.volume_24h:,.0f}")
        
        print(f"\n" + "="*80)
        print("OVERALL SUMMARY")
        print("="*80)
        print(f"📈 Total Gainers Collected: {total_gainers}")
        print(f"📉 Total Losers Collected: {total_losers}")
        print(f"🪙 Total Tokens Analyzed: {total_gainers + total_losers}")
        print(f"📊 Coverage Quality: {'✅ Excellent' if (total_gainers + total_losers) >= 150 else '⚠️ Good' if (total_gainers + total_losers) >= 100 else '❌ Limited'}")
        print("="*80)

    def export_to_csv(self, data: Dict[str, ExchangeData], filename: Optional[str] = None):
        """Export all gainers and losers from all exchanges to a CSV file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crypto_data_{timestamp}.csv"
        rows = []
        for exchange, exchange_data in data.items():
            for i, token in enumerate(exchange_data.gainers, 1):
                rows.append({
                    "exchange": exchange,
                    "type": "gainer",
                    "rank": i,
                    "symbol": token.symbol,
                    "name": token.name,
                    "price": token.price,
                    "price_change_24h": token.price_change_24h,
                    "price_change_percentage_24h": token.price_change_percentage_24h,
                    "volume_24h": token.volume_24h,
                    "market_cap": token.market_cap,
                    "timestamp": token.timestamp
                })
            for i, token in enumerate(exchange_data.losers, 1):
                rows.append({
                    "exchange": exchange,
                    "type": "loser",
                    "rank": i,
                    "symbol": token.symbol,
                    "name": token.name,
                    "price": token.price,
                    "price_change_24h": token.price_change_24h,
                    "price_change_percentage_24h": token.price_change_percentage_24h,
                    "volume_24h": token.volume_24h,
                    "market_cap": token.market_cap,
                    "timestamp": token.timestamp
                })
        fieldnames = ["exchange", "type", "rank", "symbol", "name", "price", "price_change_24h", "price_change_percentage_24h", "volume_24h", "market_cap", "timestamp"]
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        logging.info(f"Data exported to {filename}")

def main():
    """Main function to run the crypto data aggregator"""
    print("🚀 Starting Crypto Top 50 Gainers & Losers Tracker...")
    
    # Initialize the aggregator with provided API keys
    aggregator = CryptoDataAggregator(
        binance_api_key=binance_api_key,
        binance_api_secret=binance_api_secret,
        bybit_api_key=bybit_api_key,
        bybit_api_secret=bybit_api_secret
    )
    
    try:
        # Get data from all exchanges
        data = aggregator.get_all_exchange_data()
        
        # Print summary
        aggregator.print_summary(data)
        
        # Save data to file
        aggregator.save_data_to_file(data)
        
        # Export to CSV
        aggregator.export_to_csv(data)
        
        print(f"\n✅ Data collection completed successfully!")
        print(f"📁 Data saved to crypto_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json and .csv")
        
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"❌ Error occurred: {e}")

if __name__ == "__main__":
    main()
