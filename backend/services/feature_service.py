import yfinance as yf
import pandas as pd

def get_features(symbol="RELIANCE.NS"):
    try:
        df = yf.download(symbol, period="3mo", interval="1d")

        if df.empty:
            return {"error": "No data"}

        # Indicators
        df["MA_10"] = df["Close"].rolling(10).mean()
        df["MA_50"] = df["Close"].rolling(50).mean()
        df["Return"] = df["Close"].pct_change()
        df["Volatility"] = df["Return"].rolling(10).std()

        df = df.dropna()

        latest = df.iloc[-1]

        return {
            "symbol": symbol,
            "close": float(latest["Close"]),
            "ma_10": float(latest["MA_10"]),
            "ma_50": float(latest["MA_50"]),
            "volatility": float(latest["Volatility"]),
            "trend": "UP" if latest["MA_10"] > latest["MA_50"] else "DOWN"
        }

    except Exception as e:
        return {"error": str(e)}
