🛡️ AI-Powered Market Surveillance System
An end-to-end anomaly detection system designed for BFSI (Banking, Financial Services, and Insurance) environments. This system identifies suspicious stock price movements and potential market manipulation using Unsupervised Machine Learning.

🚀 Key Features
Automated Data Ingestion: Real-time extraction of NSE equity data via yfinance.

Statistical Feature Engineering: Tracks Z-Scores (volatility), Volume Ratios (liquidity spikes), and RSI (momentum).

AI Anomaly Detection: Implements an Isolation Forest model to flag non-linear patterns and outliers.

Interactive Dashboard: A Streamlit web interface for visual technical analysis and compliance monitoring.

Reporting: Generates daily Suspicious Activity Reports (SAR) in CSV format.

🛠️ Tech Stack
Language: Python 3.13

Machine Learning: Scikit-Learn (Isolation Forest)

Data Analysis: Pandas, NumPy

Visualization: Matplotlib, Streamlit

📂 Project Structure
Plaintext
NSE-MARKET-ANOMALY-DETECTION/
├── data/               # Raw market data and generated SAR reports
├── src/                # Modular logic for features and AI models
├── dashboard.py        # The Streamlit web application
└── notebooks/          # Exploratory Data Analysis (EDA)
📈 Usage
Download Data: Run the first cell in 01_exploration.ipynb.

Launch Dashboard:

Bash
python -m streamlit run dashboard.py
Analyze: Enter a ticker (e.g., RELIANCE.NS) and view detected red flags.