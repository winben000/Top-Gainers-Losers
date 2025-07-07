#!/usr/bin/env python3
"""
Example usage of Gate.io Trade Fetcher
Demonstrates how to fetch recent trades for specific tokens
"""

from gateio_trades import GateioTradeFetcher
from datetime import datetime

def example_fetch_btc_trades():
    """Example: Fetch recent BTC/USDT trades"""
    print("🔍 Example 1: Fetching BTC/USDT trades")
    print("=" * 50)
    
    fetcher = GateioTradeFetcher()
    
    # Fetch recent trades for BTC/USDT
    trades = fetcher.get_recent_trades('BTC/USDT', limit=50)
    
    if trades:
        fetcher.print_trade_summary(trades, 'BTC/USDT')
        fetcher.save_trades_to_file(trades, 'btc_trades.json')
    else:
        print("❌ No trades found for BTC/USDT")

def example_fetch_eth_trades():
    """Example: Fetch recent ETH/USDT trades"""
    print("\n🔍 Example 2: Fetching ETH/USDT trades")
    print("=" * 50)
    
    fetcher = GateioTradeFetcher()
    
    # Fetch recent trades for ETH/USDT
    trades = fetcher.get_recent_trades('ETH/USDT', limit=30)
    
    if trades:
        fetcher.print_trade_summary(trades, 'ETH/USDT')
        fetcher.save_trades_to_file(trades, 'eth_trades.json')
    else:
        print("❌ No trades found for ETH/USDT")

def example_fetch_custom_token():
    """Example: Fetch trades for a custom token"""
    print("\n🔍 Example 3: Fetching custom token trades")
    print("=" * 50)
    
    fetcher = GateioTradeFetcher()
    
    # You can change this to any token you want
    token_symbol = "SOL/USDT"  # Solana
    
    trades = fetcher.get_recent_trades(token_symbol, limit=25)
    
    if trades:
        fetcher.print_trade_summary(trades, token_symbol)
        fetcher.save_trades_to_file(trades, f'{token_symbol.replace("/", "_")}_trades.json')
    else:
        print(f"❌ No trades found for {token_symbol}")

def example_timeframe_trades():
    """Example: Fetch trades within a specific timeframe"""
    print("\n🔍 Example 4: Fetching trades within timeframe")
    print("=" * 50)
    
    fetcher = GateioTradeFetcher()
    
    # Fetch trades in the last 1 hour
    trades = fetcher.get_trades_with_timeframe('BTC/USDT', timeframe='1h', limit=100)
    
    if trades:
        fetcher.print_trade_summary(trades, 'BTC/USDT (Last 1h)')
        fetcher.save_trades_to_file(trades, 'btc_1h_trades.json')
    else:
        print("❌ No trades found for BTC/USDT in last 1h")

def example_get_available_tokens():
    """Example: Get list of available tokens"""
    print("\n🔍 Example 5: Available USDT trading pairs")
    print("=" * 50)
    
    fetcher = GateioTradeFetcher()
    
    symbols = fetcher.get_available_symbols()
    
    print("📋 Available USDT trading pairs:")
    for i, symbol in enumerate(symbols, 1):
        print(f"{i:2d}. {symbol}")

def main():
    """Run all examples"""
    print("🚀 Gate.io Trade Fetcher Examples")
    print("=" * 60)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Run examples
        example_get_available_tokens()
        example_fetch_btc_trades()
        example_fetch_eth_trades()
        example_fetch_custom_token()
        example_timeframe_trades()
        
        print(f"\n✅ All examples completed successfully!")
        print(f"📁 Check the generated JSON files for trade data")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")

if __name__ == "__main__":
    main() 