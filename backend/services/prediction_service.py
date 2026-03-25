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

        # 🔥 Get sentiment
        sentiment_data = get_sentiment(symbol)
        sentiment = sentiment_data.get("sentiment", "NEUTRAL")

        # 🔥 ML Prediction
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

            # Keep confidence within bounds
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


# 🚀 ⭐ Top AI Picks (Multi-stock ranking)
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
            "top_picks": results[:3],  # Top 3 best stocks
            "all": results
        }

    except Exception as e:
        return {"error": str(e)}
