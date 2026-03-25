import yfinance as yf

def get_stock_data(symbol="RELIANCE.NS"):
    try:
        df = yf.download(symbol, period="1mo", interval="1d")

        if df.empty:
            return {"error": "No data found"}

        latest = df.iloc[-1]

        return {
            "symbol": symbol,
            "open": float(latest["Open"].item()),
            "high": float(latest["High"].item()),
            "low": float(latest["Low"].item()),
            "close": float(latest["Close"].item()),
            "volume": int(latest["Volume"].item())
        }

    except Exception as e:
        return {"error": str(e)}
