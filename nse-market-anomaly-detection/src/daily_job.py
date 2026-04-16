import pandas as pd
import time
from src.features import calculate_features
from src.anomaly_models import train_anomaly_detector
from src.database import init_db, log_alerts
from src.alerts import send_anomaly_email

def run_daily_pipeline():
    print("🚀 Starting Daily MarketSentinel AI Pipeline...")
    
    # 1. Initialize Database
    init_db()
    
    # 2. Load Raw Data (In production, this would use yfinance to fetch today's data)
    # yf.download("RELIANCE.NS TCS.NS INF.NS ...", period="1y")
    try:
        df_raw = pd.read_csv('data/nifty_raw_data.csv', index_col=0, header=[0,1])
    except Exception as e:
        print(f"❌ Failed to load market data: {e}")
        return

    tickers = df_raw.columns.get_level_values(1).unique()
    print(f"Tracking {len(tickers)} assets.")
    
    total_alerts_today = 0
    
    for ticker in tickers:
        print(f"Processing {ticker}...")
        try:
            ticker_data = df_raw.xs(ticker, axis=1, level=1).copy()
            
            # Step A: Engineering
            processed_df = calculate_features(ticker_data)
            
            # Step B: AI Detection
            final_df, model, explainer, shap_values = train_anomaly_detector(processed_df)
            
            # Step C: Filter Anomalies
            anomalies = final_df[final_df['anomaly_signal'] == -1]
            
            if len(anomalies) > 0:
                # Get the most recent anomaly if it happened "today" (last row)
                last_date = anomalies.index[-1]
                last_price = anomalies.iloc[-1]['Close']
                
                # Log to DB
                log_alerts(ticker, anomalies)
                total_alerts_today += len(anomalies)
                
                # Optional: Send Email (Commented to prevent spam during local tests)
                # send_anomaly_email(ticker, len(anomalies), last_price)
                
        except Exception as e:
            print(f"⚠️ Error processing {ticker}: {e}")
            
    print(f"✅ Pipeline Completed. Total Alerts Identified and Logged: {total_alerts_today}")

if __name__ == "__main__":
    run_daily_pipeline()
