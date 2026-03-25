from backend.services.feature_service import get_features
from backend.services.ml_service import ml_predict
from backend.services.sentiment_service import get_sentiment


# 🎯 Single stock prediction
def predict_signal(symbol="RELIANCE.NS"):
    try:
        data = get_features(symbol)

        if "error" in data:
            return data

        trend = data["trend"]
        volatility = data["volatility"]

        # 🌍 Get sentiment
        sentiment_data = get_sentiment(symbol)
        sentiment = sentiment_data.get("sentiment", "NEUTRAL")

        # 🧠 ML Prediction
        ml_signal = ml_predict(data)

        if ml_signal:
            signal = ml_signal
            confidence = 80

            # 🌍 Adjust using sentiment
            if sentiment == "POSITIVE" and signal == "BUY":
                confidence += 5
            elif sentiment == "NEGATIVE" and signal == "SELL":
                confidence += 5
            elif sentiment == "NEGATIVE" and signal == "BUY":
                confidence -= 10
            elif sentiment == "POSITIVE" and signal == "SELL":
                confidence -= 10

            confidence = max(0, min(100, confidence))
            source = "ML + Sentiment"

        else:
            # 🔁 Fallback Logic
            if trend == "UP" and volatility < 0.02:
                signal = "BUY"
                confidence = 70
            elif trend == "DOWN" and volatility < 0.02:
                signal = "SELL"
                confidence = 70
            else:
                signal = "HOLD"
                confidence = 50

            source = "Rule-based"

        return {
            "symbol": symbol,
            "prediction": signal,
            "confidence": confidence,
            "source": source,
            "sentiment": sentiment,
            "reason": {
                "trend": trend,
                "volatility": volatility
            }
        }

    except Exception as e:
        return {"error": str(e)}


# ⭐ Top AI Picks (Multi-stock ranking)
def get_top_picks():
    try:
        stocks = ["AAPL", "TSLA", "RELIANCE.NS", "TCS.NS", "INFY.NS"]

        results = []

        for symbol in stocks:
            result = predict_signal(symbol)

            if "error" not in result:
                results.append(result)

        # 🔥 Sort by confidence (highest first)
        results = sorted(results, key=lambda x: x["confidence"], reverse=True)

        return {
            "top_picks": results[:3],
            "all": results
        }

    except Exception as e:
        return {"error": str(e)}


# 💰 Portfolio AI (ONLY BUY stocks)
def get_portfolio():
    try:
        picks_data = get_top_picks()
        picks = picks_data.get("top_picks", [])

        # ✅ Filter only BUY stocks
        buy_stocks = [s for s in picks if s["prediction"] == "BUY"]

        if not buy_stocks:
            return {"error": "No BUY opportunities found"}

        total_confidence = sum([stock["confidence"] for stock in buy_stocks])

        portfolio = []

        for stock in buy_stocks:
            allocation = (stock["confidence"] / total_confidence) * 100

            portfolio.append({
                "symbol": stock["symbol"],
                "prediction": stock["prediction"],
                "allocation": round(allocation, 2)
            })

        return {
            "portfolio": portfolio
        }

    except Exception as e:
        return {"error": str(e)}
