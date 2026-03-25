import os
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml_models", "lstm_model.h5")

def load_lstm():
    try:
        if os.path.exists(MODEL_PATH):
            print("✅ LSTM model loaded")
            return load_model(MODEL_PATH)
        else:
            print("❌ LSTM model not found")
            return None
    except Exception as e:
        print("LSTM load error:", e)
        return None

model = load_lstm()

def lstm_predict(symbol="AAPL"):
    try:
        if model is None:
            return None

        df = yf.download(symbol, period="3mo")

        data = df["Close"].values.reshape(-1, 1)

        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(data)

        seq_len = 50

        if len(data_scaled) < seq_len:
            return None

        X = []
        for i in range(seq_len, len(data_scaled)):
            X.append(data_scaled[i-seq_len:i])

        X = np.array(X)

        last_sequence = X[-1].reshape(1, seq_len, 1)

        pred = model.predict(last_sequence)[0][0]

        return "BUY" if pred > 0.5 else "SELL"

    except Exception as e:
        print("LSTM prediction error:", e)
        return None
