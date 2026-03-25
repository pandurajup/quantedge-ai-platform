from backend.services.feature_service import get_features
from backend.services.ml_service import ml_predict

def predict_signal(symbol="RELIANCE.NS"):
    try:
        data = get_features(symbol)

        # Handle error from feature service
        if "error" in data:
            return data

        trend = data["trend"]
        volatility = data["volatility"]

        # 🔥 ML Prediction (Primary)
        ml_signal = ml_predict(data)

        if ml_signal:
            signal = ml_signal
            confidence = 80
            source = "ML Model"
        else:
            # 🔁 Fallback Logic (Rule-based)
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
            "reason": {
                "trend": trend,
                "volatility": volatility
            }
        }

    except Exception as e:
        return {"error": str(e)}
