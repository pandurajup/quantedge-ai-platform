import yfinance as yf

def get_stock_data(symbol="RELIANCE.NS"):
    try:
        df = yf.download(symbol, period="1mo", interval="1d")

        if df.empty:
            return {"error": "No data found"}

        latest = df.tail(1)

        return {
            "symbol": symbol,
            "open": float(latest["Open"].values[0]),
            "high": float(latest["High"].values[0]),
            "low": float(latest["Low"].values[0]),
            "close": float(latest["Close"].values[0]),
            "volume": int(latest["Volume"].values[0])
        }

    except Exception as e:
        return {"error": str(e)}
