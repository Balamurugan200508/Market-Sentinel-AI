import pandas as pd
import shap
from sklearn.ensemble import IsolationForest

def train_anomaly_detector(df):
    """
    Trains an Isolation Forest to detect market manipulation and uses SHAP to explain anomalies.
    """
    # Define the features the model will look at (now including MACD and VPT)
    features = ['z_score', 'volume_ratio', 'volatility', 'rsi', 'macd_hist', 'vpt']
    X = df[features]

    # Initialize Model
    # contamination=0.01 means we expect roughly 1% of data to be 'manipulated/anomalous'
    model = IsolationForest(contamination=0.01, random_state=42)
    
    # Fit the model and predict
    # 1 = normal, -1 = anomaly
    df['anomaly_signal'] = model.fit_predict(X)
    
    # Calculate SHAP values for explainability
    # IsolationForest works with TreeExplainer
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    
    return df, model, explainer, shap_values

if __name__ == "__main__":
    print("Model logic initialized. Ready for training.")