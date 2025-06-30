#!/usr/bin/env python3
"""
Data Statistics Analyzer for Crypto Top 50 Gainers & Losers
Analyzes the collected data and provides insights
"""

import json
import glob
from datetime import datetime
from typing import Dict, List, Any

def analyze_latest_data():
    """Analyze the most recent data file"""
    
    # Find the most recent data file
    data_files = glob.glob("crypto_data_*.json")
    if not data_files:
        print("❌ No data files found. Run the main script first.")
        return
    
    # Get the most recent file
    latest_file = max(data_files, key=lambda x: x.split('_')[2].split('.')[0])
    print(f"📊 Analyzing data from: {latest_file}")
    
    with open(latest_file, 'r') as f:
        data = json.load(f)
    
    print("\n" + "="*80)
    print("CRYPTO DATA ANALYSIS SUMMARY")
    print("="*80)
    
    total_gainers = 0
    total_losers = 0
    total_tokens = 0
    
    for exchange_name, exchange_data in data.items():
        if not exchange_data.get("success", False):
            continue
            
        gainers = exchange_data.get("gainers", [])
        losers = exchange_data.get("losers", [])
        
        total_gainers += len(gainers)
        total_losers += len(losers)
        total_tokens += len(gainers) + len(losers)
        
        print(f"\n{exchange_name.upper()} EXCHANGE:")
        print("-" * 40)
        print(f"✅ Success: {exchange_data.get('success', False)}")
        print(f"📊 Gainers: {len(gainers)} tokens")
        print(f"📉 Losers: {len(losers)} tokens")
        print(f"🕒 Timestamp: {exchange_data.get('timestamp', 'N/A')}")
        
        if gainers:
            best_gainer = max(gainers, key=lambda x: x.get('price_change_percentage_24h', 0))
            print(f"🏆 Best Gainer: {best_gainer.get('symbol', 'N/A')} (+{best_gainer.get('price_change_percentage_24h', 0):.2f}%)")
        
        if losers:
            worst_loser = min(losers, key=lambda x: x.get('price_change_percentage_24h', 0))
            print(f"📉 Worst Loser: {worst_loser.get('symbol', 'N/A')} ({worst_loser.get('price_change_percentage_24h', 0):.2f}%)")
    
    print(f"\n" + "="*80)
    print("OVERALL STATISTICS")
    print("="*80)
    print(f"📈 Total Gainers: {total_gainers}")
    print(f"📉 Total Losers: {total_losers}")
    print(f"🪙 Total Tokens Analyzed: {total_tokens}")
    print(f"📊 Data Quality: {'✅ Excellent' if total_tokens >= 150 else '⚠️ Good' if total_tokens >= 100 else '❌ Limited'}")
    
    # Analyze gainers across all exchanges
    all_gainers = []
    all_losers = []
    
    for exchange_data in data.values():
        if exchange_data.get("success", False):
            all_gainers.extend(exchange_data.get("gainers", []))
            all_losers.extend(exchange_data.get("losers", []))
    
    if all_gainers:
        top_gainers = sorted(all_gainers, key=lambda x: x.get('price_change_percentage_24h', 0), reverse=True)[:10]
        print(f"\n🏆 TOP 10 GAINERS ACROSS ALL EXCHANGES:")
        for i, token in enumerate(top_gainers, 1):
            print(f"  {i:2d}. {token.get('symbol', 'N/A'):<8} ({token.get('exchange', 'N/A'):<10}) +{token.get('price_change_percentage_24h', 0):.2f}%")
    
    if all_losers:
        top_losers = sorted(all_losers, key=lambda x: x.get('price_change_percentage_24h', 0))[:10]
        print(f"\n📉 TOP 10 LOSERS ACROSS ALL EXCHANGES:")
        for i, token in enumerate(top_losers, 1):
            print(f"  {i:2d}. {token.get('symbol', 'N/A'):<8} ({token.get('exchange', 'N/A'):<10}) {token.get('price_change_percentage_24h', 0):.2f}%")

def analyze_data_files():
    """Analyze all available data files"""
    
    data_files = glob.glob("crypto_data_*.json")
    if not data_files:
        print("❌ No data files found.")
        return
    
    print(f"📁 Found {len(data_files)} data files")
    
    # Sort files by timestamp
    sorted_files = sorted(data_files, key=lambda x: x.split('_')[2].split('.')[0])
    
    print(f"\n📅 Data Collection History:")
    for i, file in enumerate(sorted_files[-5:], 1):  # Show last 5 files
        timestamp = file.split('_')[2].split('.')[0]
        try:
            dt = datetime.strptime(timestamp, "%Y%m%d%H%M%S")
            print(f"  {i}. {dt.strftime('%Y-%m-%d %H:%M:%S')} - {file}")
        except:
            print(f"  {i}. {timestamp} - {file}")

if __name__ == "__main__":
    print("🔍 Crypto Data Statistics Analyzer")
    print("="*50)
    
    analyze_data_files()
    print("\n")
    analyze_latest_data() 