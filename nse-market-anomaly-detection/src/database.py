import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_PATH = "data/market_sentinel.db"

def init_db():
    """Initializes the SQLite database and creates the necessary tables if they don't exist."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create Alerts Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            date TEXT,
            close_price REAL,
            z_score REAL,
            volume_ratio REAL,
            rsi REAL,
            volatility REAL,
            macd_hist REAL,
            vpt REAL,
            anomaly_signal INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def log_alerts(ticker, df_anomalies):
    """Logs detected anomalies into the SQLite database."""
    if df_anomalies.empty:
        return
        
    conn = sqlite3.connect(DB_PATH)
    
    # Prepare dataframe for SQL
    df_insert = df_anomalies.copy()
    df_insert['ticker'] = ticker
    df_insert['date'] = df_insert.index.astype(str) # Convert DatetimeIndex to string
    
    # Keep only columns we want to insert
    columns_to_keep = ['ticker', 'date', 'Close', 'z_score', 'volume_ratio', 'rsi', 'volatility', 'macd_hist', 'vpt', 'anomaly_signal']
    df_insert = df_insert[columns_to_keep].rename(columns={'Close': 'close_price'})
    
    # Append to SQLite table
    df_insert.to_sql('alerts', conn, if_exists='append', index=False)
    
    conn.close()
    print(f"Logged {len(df_insert)} alerts for {ticker} into database.")

def fetch_recent_alerts(limit=50):
    """Fetches the most recent alerts across all tickers."""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?"
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df

if __name__ == "__main__":
    init_db()
