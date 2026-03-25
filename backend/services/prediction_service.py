from backend.services.feature_service import get_features
from backend.services.ml_service import ml_predict
from backend.services.lstm_service import lstm_predict


def predict_signal(symbol="RELIANCE.NS"):
    try:
        # 🔹 Get features
        data = get_features(symbol)

        if "error" in data:
            return data

        trend = data["trend"]
        volatility = data["volatility"]

        # 🔥 Get predictions from both models
        ml_signal = ml_predict(data)
        lstm_signal = lstm_predict(symbol)

        # 🔥 Collect signals
        signals = []

        if ml_signal:
            signals.append(ml_signal)

        if lstm_signal:
            signals.append(lstm_signal)

        # 🔥 Ensemble Decision
        buy_count = signals.count("BUY")
        sell_count = signals.count("SELL")

        if buy_count > sell_count:
            signal = "BUY"
            confidence = 85
            source = "Ensemble AI"
        elif sell_count > buy_count:
            signal = "SELL"
            confidence = 85
            source = "Ensemble AI"
        else:
            # 🔁 Fallback Logic (if models disagree or fail)
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
            "details": {
                "ml": ml_signal,
                "lstm": lstm_signal
            },
            "reason": {
                "trend": trend,
                "volatility": volatility
            }
        }

    except Exception as e:
        return {"error": str(e)}
