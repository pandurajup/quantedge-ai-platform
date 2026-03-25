from backend.services.feature_service import get_features

def predict_signal(symbol="RELIANCE.NS"):
    try:
        data = get_features(symbol)

        if "error" in data:
            return data

        trend = data["trend"]
        volatility = data["volatility"]

        # Basic decision logic (will evolve later)
        if trend == "UP" and volatility < 0.02:
            signal = "BUY"
            confidence = 70
        elif trend == "DOWN" and volatility < 0.02:
            signal = "SELL"
            confidence = 70
        else:
            signal = "HOLD"
            confidence = 50

        return {
            "symbol": symbol,
            "prediction": signal,
            "confidence": confidence,
            "reason": {
                "trend": trend,
                "volatility": volatility
            }
        }

    except Exception as e:
        return {"error": str(e)}
