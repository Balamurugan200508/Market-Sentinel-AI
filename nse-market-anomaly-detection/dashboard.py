import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import shap
import matplotlib.pyplot as plt
from src.features import calculate_features
from src.anomaly_models import train_anomaly_detector

st.set_page_config(page_title="MarketSentinel AI", layout="wide")

st.title("🛡️ MarketSentinel AI Surveillance")
st.sidebar.header("Settings")

# Sidebar - Ticker Selection
ticker_input = st.sidebar.text_input("Enter Ticker (e.g. RELIANCE.NS)", "^NSEI")

if st.sidebar.button("Run Analysis"):
    # Load data from our saved file
    df_raw = pd.read_csv('data/nifty_raw_data.csv', index_col=0, header=[0,1])
    
    if ticker_input in df_raw.columns.get_level_values(1):
        ticker_data = df_raw.xs(ticker_input, axis=1, level=1).copy()
        
        # Run Pipeline
        processed_df = calculate_features(ticker_data)
        final_df, model, explainer, shap_values = train_anomaly_detector(processed_df)
        
        # Display Stats
        anomalies = final_df[final_df['anomaly_signal'] == -1]
        col1, col2 = st.columns(2)
        col1.metric("Total Days Analyzed", len(final_df))
        col2.metric("Red Flag Alerts", len(anomalies), delta_color="inverse")

        # Plotting with Plotly
        st.subheader(f"Price Chart: {ticker_input}")
        fig = go.Figure()
        
        # Add Close Price line
        fig.add_trace(go.Scatter(x=final_df.index, y=final_df['Close'],
                            mode='lines',
                            name='Price',
                            line=dict(color='blue')))
        
        # Add Anomaly markers
        fig.add_trace(go.Scatter(x=anomalies.index, y=anomalies['Close'],
                            mode='markers',
                            name='AI Alert',
                            marker=dict(color='red', size=10, symbol='x')))
        
        fig.update_layout(title='Interactive Price & Anomaly Chart',
                          xaxis_title='Date',
                          yaxis_title='Close Price')
        st.plotly_chart(fig, use_container_width=True)
        
        # Explainability Section
        st.subheader("🧠 Why was this flagged? (Explainable AI)")
        if len(anomalies) > 0:
            st.write("SHAP values show the impact of each feature on the model's output. Features pushing the prediction lower (towards -1) contributed to the anomaly flag.")
            
            # We generate a SHAP summary plot for the anomalies
            # Plotting SHAP in Streamlit requires matplotlib
            fig_shap, ax_shap = plt.subplots(figsize=(10, 5))
            features = ['z_score', 'volume_ratio', 'volatility', 'rsi', 'macd_hist', 'vpt']
            X_anomalies = anomalies[features]
            shap_anomalies = explainer.shap_values(X_anomalies)
            
            shap.summary_plot(shap_anomalies, X_anomalies, show=False)
            st.pyplot(fig_shap)
        else:
            st.info("No anomalies detected to explain.")

        # Table of Alerts
        st.subheader("Recent Alerts Data")
        st.dataframe(anomalies.tail())
    else:
        st.error("Ticker not found in local data. Run the downloader first.")