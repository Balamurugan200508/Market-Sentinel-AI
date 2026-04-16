import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_anomaly_email(ticker, alert_count, last_price):
    # --- CONFIGURATION ---
    sender_email = "your_email@gmail.com" 
    receiver_email = "your_email@gmail.com"
    password = "your_app_password" # This is NOT your login password, it's a Google App Password
    
    # --- MESSAGE ---
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"🚨 MARKET ALERT: {ticker} Suspicious Activity"

    body = f"""
    Market Surveillance Alert:
    --------------------------
    Asset: {ticker}
    Anomalies Detected: {alert_count}
    Latest Close Price: {last_price:.2f}
    
    The AI model has detected unusual volume and price movement. 
    Check the Surveillance Report for details.
    """
    message.attach(MIMEText(body, "plain"))

    # --- SENDING ---
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"✅ Email alert sent for {ticker}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")