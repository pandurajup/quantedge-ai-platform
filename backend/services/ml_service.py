import pickle
import os

MODEL_PATH = "ml_models/model.pkl"

def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    return None

model = load_model()

def ml_predict(features):
    if model is None:
        return None

    try:
        X = [[
            features["close"],
            features["ma_10"],
            features["ma_50"],
            features["volatility"]
        ]]

        pred = model.predict(X)[0]

        return "BUY" if pred == 1 else "SELL"

    except:
        return None
