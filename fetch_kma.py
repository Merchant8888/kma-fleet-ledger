import ccxt
import pandas as pd
import time

def fetch_kma_matrix(symbol='ETH/USDT', timeframe='4h', limit=300):
    """
    Decoupled Web3 Data Engine: Fetches clean structural market candles
    and computes the timeframe-agnostic 21/200 KMA parameters natively.
    """
    exchange = ccxt.mexc({
        'enableRateLimit': True,
        'options': {'defaultType': 'swap'} 
    })
    
    try:
        print(f"📡 Establishing connection to Web3 order book for {symbol} ({timeframe})...")
        raw_candles = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        
        df = pd.DataFrame(raw_candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        df['21_KMA'] = df['close'].rolling(window=21).mean()
        df['200_KMA'] = df['close'].rolling(window=200).mean()
        
        latest_candle = df.iloc[-1]
        current_close = latest_candle['close']
        kma21 = latest_candle['21_KMA']
        kma200 = latest_candle['200_KMA']
        
        print("\n" + "="*50)
        print(f"📊 LIVE CORE DATA LOG FOR {symbol} [{timeframe.upper()}]")
        print("="*50)
        print(f"• Current Asset Fair Price:  ${current_close:,.2f}")
        print(f"• System 21 KMA Floor/Roof:  ${kma21:,.2f}")
        print(f"• System 200 KMA Base Anchor: ${kma200:,.2f}")
        print("-"*50)
        
        if current_close > kma21:
            print("🚀 STATUS: BULLISH EXPANSION — Price holding above 21 KMA support floor.")
        else:
            print("📉 STATUS: BEARISH COMPRESSION — Price trapped beneath 21 KMA overhead roof.")
            
        return df
        
    except Exception as e:
        print(f"❌ Structural Connection Interrupted: {e}")
        return None

if __name__ == '__main__':
    fetch_kma_matrix(symbol='ETH/USDT', timeframe='4h')
