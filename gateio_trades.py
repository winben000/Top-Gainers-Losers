#!/usr/bin/env python3
"""
Gate.io Trade Data Fetcher
Fetches recent trades for a specific token using CCXT library
"""

import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class GateioTradeFetcher:
    """Gate.io trade data fetcher using CCXT"""
    
    def __init__(self, api_key: Optional[str] = None, secret: Optional[str] = None):
        """
        Initialize Gate.io exchange connection
        
        Args:
            api_key: Gate.io API key (optional for public data)
            secret: Gate.io secret key (optional for public data)
        """
        self.exchange = ccxt.gateio({
            'apiKey': api_key or os.getenv('GATEIO_API_KEY'),
            'secret': secret or os.getenv('GATEIO_SECRET'),
            'sandbox': False,  # Set to True for testing
            'enableRateLimit': True,
        })
        
        print(f"🔗 Connected to Gate.io exchange")
        print(f"📊 Exchange: {self.exchange.name}")
        print(f"🌐 URL: {self.exchange.urls['api']}")
    
    def get_recent_trades(self, symbol: str, limit: int = 100) -> List[Dict]:
        """
        Fetch recent trades for a specific symbol
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTC/USDT', 'ETH/USDT')
            limit: Number of trades to fetch (default: 100, max: 1000)
            
        Returns:
            List of trade dictionaries
        """
        try:
            print(f"📈 Fetching recent trades for {symbol}...")
            
            # Fetch recent trades
            trades = self.exchange.fetch_trades(symbol, limit=limit)
            
            print(f"✅ Successfully fetched {len(trades)} trades for {symbol}")
            
            # Process and format trades
            formatted_trades = []
            for trade in trades:
                formatted_trade = {
                    'id': trade['id'],
                    'timestamp': trade['timestamp'],
                    'datetime': trade['datetime'],
                    'symbol': trade['symbol'],
                    'side': trade['side'],  # 'buy' or 'sell'
                    'amount': trade['amount'],
                    'price': trade['price'],
                    'cost': trade['cost'],
                    'fee': trade.get('fee', {}),
                    'order': trade.get('order'),
                    'type': trade.get('type'),
                    'takerOrMaker': trade.get('takerOrMaker'),
                }
                formatted_trades.append(formatted_trade)
            
            return formatted_trades
            
        except Exception as e:
            print(f"❌ Error fetching trades for {symbol}: {e}")
            return []
    
    def get_trades_with_timeframe(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> List[Dict]:
        """
        Fetch trades within a specific timeframe
        
        Args:
            symbol: Trading pair symbol
            timeframe: Timeframe ('1m', '5m', '15m', '1h', '4h', '1d')
            limit: Number of trades to fetch
            
        Returns:
            List of trades within the timeframe
        """
        try:
            # Calculate time range
            now = datetime.now()
            timeframe_minutes = {
                '1m': 1, '5m': 5, '15m': 15, '30m': 30,
                '1h': 60, '4h': 240, '1d': 1440
            }
            
            minutes = timeframe_minutes.get(timeframe, 60)
            start_time = now - timedelta(minutes=minutes)
            
            print(f"📈 Fetching trades for {symbol} in last {timeframe}...")
            
            # Fetch trades
            trades = self.exchange.fetch_trades(symbol, limit=limit)
            
            # Filter trades by timeframe
            filtered_trades = []
            for trade in trades:
                trade_time = datetime.fromtimestamp(trade['timestamp'] / 1000)
                if trade_time >= start_time:
                    filtered_trades.append(trade)
            
            print(f"✅ Found {len(filtered_trades)} trades in last {timeframe}")
            return filtered_trades
            
        except Exception as e:
            print(f"❌ Error fetching trades with timeframe: {e}")
            return []
    
    def get_trade_statistics(self, trades: List[Dict]) -> Dict:
        """
        Calculate statistics from trade data
        
        Args:
            trades: List of trade dictionaries
            
        Returns:
            Dictionary with trade statistics
        """
        if not trades:
            return {}
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(trades)
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Calculate statistics
        stats = {
            'total_trades': len(trades),
            'total_volume': df['amount'].sum(),
            'total_value': df['cost'].sum(),
            'avg_price': df['price'].mean(),
            'min_price': df['price'].min(),
            'max_price': df['price'].max(),
            'price_volatility': df['price'].std(),
            'buy_trades': len(df[df['side'] == 'buy']),
            'sell_trades': len(df[df['side'] == 'sell']),
            'buy_volume': df[df['side'] == 'buy']['amount'].sum(),
            'sell_volume': df[df['side'] == 'sell']['amount'].sum(),
            'time_range': {
                'start': df['datetime'].min().isoformat(),
                'end': df['datetime'].max().isoformat()
            }
        }
        
        return stats
    
    def save_trades_to_file(self, trades: List[Dict], filename: Optional[str] = None):
        """
        Save trades to JSON file
        
        Args:
            trades: List of trade dictionaries
            filename: Output filename (optional)
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"gateio_trades_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(trades, f, indent=2, default=str)
            print(f"💾 Trades saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving trades: {e}")
    
    def print_trade_summary(self, trades: List[Dict], symbol: str):
        """
        Print a summary of the trades
        
        Args:
            trades: List of trade dictionaries
            symbol: Trading pair symbol
        """
        if not trades:
            print("❌ No trades to display")
            return
        
        stats = self.get_trade_statistics(trades)
        
        print(f"\n{'='*60}")
        print(f"📊 TRADE SUMMARY FOR {symbol}")
        print(f"{'='*60}")
        print(f"📈 Total Trades: {stats['total_trades']}")
        print(f"💰 Total Volume: {stats['total_volume']:.6f}")
        print(f"💵 Total Value: ${stats['total_value']:,.2f}")
        print(f"📊 Average Price: ${stats['avg_price']:.6f}")
        print(f"📉 Min Price: ${stats['min_price']:.6f}")
        print(f"📈 Max Price: ${stats['max_price']:.6f}")
        print(f"📊 Price Volatility: ${stats['price_volatility']:.6f}")
        print(f"🟢 Buy Trades: {stats['buy_trades']} (Volume: {stats['buy_volume']:.6f})")
        print(f"🔴 Sell Trades: {stats['sell_trades']} (Volume: {stats['sell_volume']:.6f})")
        print(f"⏰ Time Range: {stats['time_range']['start']} to {stats['time_range']['end']}")
        print(f"{'='*60}")
        
        # Show recent trades
        print(f"\n🕒 RECENT TRADES:")
        print(f"{'Time':<20} {'Side':<6} {'Price':<12} {'Amount':<12} {'Value':<15}")
        print("-" * 70)
        
        for trade in trades[:10]:  # Show last 10 trades
            trade_time = datetime.fromtimestamp(trade['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            side_emoji = "🟢" if trade['side'] == 'buy' else "🔴"
            print(f"{trade_time:<20} {side_emoji} {trade['side']:<4} ${trade['price']:<10.6f} {trade['amount']:<11.6f} ${trade['cost']:<13.2f}")
    
    def get_available_symbols(self) -> List[str]:
        """
        Get list of available trading symbols
        
        Returns:
            List of available symbols
        """
        try:
            markets = self.exchange.load_markets()
            usdt_pairs = [symbol for symbol in markets.keys() if symbol.endswith('/USDT')]
            return usdt_pairs[:20]  # Return first 20 for display
        except Exception as e:
            print(f"❌ Error fetching symbols: {e}")
            return []

def main():
    """Main function to demonstrate usage"""
    print("🚀 Gate.io Trade Data Fetcher")
    print("=" * 40)
    
    # Initialize fetcher
    fetcher = GateioTradeFetcher()
    
    # Get available symbols
    print("\n📋 Available USDT pairs (first 20):")
    symbols = fetcher.get_available_symbols()
    for i, symbol in enumerate(symbols, 1):
        print(f"{i:2d}. {symbol}")
    
    # Example: Fetch trades for a specific token
    symbol = input(f"\n🎯 Enter symbol to fetch trades (e.g., BTC/USDT): ").strip().upper()
    
    if not symbol:
        symbol = "BTC/USDT"  # Default
    
    # Add /USDT if not provided
    if not symbol.endswith('/USDT'):
        symbol += '/USDT'
    
    # Fetch recent trades
    trades = fetcher.get_recent_trades(symbol, limit=100)
    
    if trades:
        # Print summary
        fetcher.print_trade_summary(trades, symbol)
        
        # Save to file
        fetcher.save_trades_to_file(trades)
        
        # Get statistics
        stats = fetcher.get_trade_statistics(trades)
        print(f"\n📊 Trade Statistics saved to file")
        
    else:
        print(f"❌ No trades found for {symbol}")

if __name__ == "__main__":
    main() 