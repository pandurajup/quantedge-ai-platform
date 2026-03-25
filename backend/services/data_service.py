import yfinance as yf


# 📊 Stock data (latest OHLC)
def get_stock_data(symbol="RELIANCE.NS"):
    try:
        df = yf.download(symbol, period="1mo", interval="1d")

        if df.empty:
            return {"error": "No data found"}

        df = df.reset_index()
        latest = df.iloc[-1]

        def safe_float(value):
            try:
                if hasattr(value, "values"):
                    return float(value.values[0])
                return float(value)
            except:
                return None

        return {
            "symbol": symbol,
            "open": safe_float(latest["Open"]),
            "high": safe_float(latest["High"]),
            "low": safe_float(latest["Low"]),
            "close": safe_float(latest["Close"]),
            "volume": int(safe_float(latest["Volume"]) or 0)
        }

    except Exception as e:
        return {"error": str(e)}


# 📈 Chart data (fixed version)
def get_chart_data(symbol="AAPL"):
    try:
        df = yf.download(symbol, period="1mo", interval="1d")

        if df.empty:
            return {"error": "No data found"}

        # ✅ Fix: Ensure Close is handled correctly
        close = df["Close"]

        if hasattr(close, "values"):
            prices = close.values.flatten().tolist()
        else:
            prices = []

        dates = df.index.strftime("%Y-%m-%d").tolist()

        return {
            "dates": dates,
            "prices": prices
        }

    except Exception as e:
        return {"error": str(e)}
