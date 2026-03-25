import yfinance as yf

def get_features(symbol="RELIANCE.NS"):
    try:
        df = yf.download(symbol, period="3mo", interval="1d")

        if df.empty:
            return {"error": "No data"}

        # Reset index (important fix)
        df = df.reset_index()

        # Indicators
        df["MA_10"] = df["Close"].rolling(10).mean()
        df["MA_50"] = df["Close"].rolling(50).mean()
        df["Return"] = df["Close"].pct_change()
        df["Volatility"] = df["Return"].rolling(10).std()

        df = df.dropna()

        latest = df.iloc[-1]

        def safe_float(value):
            try:
                if hasattr(value, "values"):
                    return float(value.values[0])
                return float(value)
            except:
                return None

        ma10 = safe_float(latest["MA_10"])
        ma50 = safe_float(latest["MA_50"])

        return {
            "symbol": symbol,
            "close": safe_float(latest["Close"]),
            "ma_10": ma10,
            "ma_50": ma50,
            "volatility": safe_float(latest["Volatility"]),
            "trend": "UP" if ma10 and ma50 and ma10 > ma50 else "DOWN"
        }

    except Exception as e:
        return {"error": str(e)}
