import pandas as pd
import numpy as np

def calculate_features(df):
    """
    Upgraded feature engineering with RSI, Volatility, MACD, and Volume-Price Trend (VPT).
    """
    df = df.copy()
    
    # 1. Z-Score (Price Deviation)
    df['price_mean'] = df['Close'].rolling(window=20).mean()
    df['price_std'] = df['Close'].rolling(window=20).std()
    df['z_score'] = (df['Close'] - df['price_mean']) / df['price_std']

    # 2. Volume Ratio
    df['vol_mean'] = df['Volume'].rolling(window=20).mean()
    df['volume_ratio'] = df['Volume'] / df['vol_mean']

    # 3. RSI (Relative Strength Index)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # 4. Volatility (Rolling Std Dev of returns)
    df['volatility'] = df['Close'].pct_change().rolling(window=20).std()

    # 5. MACD (Moving Average Convergence Divergence)
    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema_12 - ema_26
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['macd_hist'] = df['macd'] - df['macd_signal']

    # 6. VPT (Volume-Price Trend)
    # VPT = Previous VPT + Volume * (Current Close - Previous Close) / Previous Close
    pct_change = df['Close'].pct_change()
    vpt = (df['Volume'] * pct_change).cumsum()
    df['vpt'] = vpt

    # Clean up NaN values
    df = df.dropna()
    
    return df