import pickle
import os

# 🔥 Get absolute base directory (important for deployment)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# 🔥 Correct model path
MODEL_PATH = os.path.join(BASE_DIR, "ml_models", "model.pkl")


def load_model():
    try:
        print("🔍 Looking for model at:", MODEL_PATH)

        if os.path.exists(MODEL_PATH):
            print("✅ Model file found")

            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)

            print("✅ Model loaded successfully")
            return model
        else:
            print("❌ Model file NOT found")

    except Exception as e:
        print(f"❌ Error loading model: {e}")

    return None


# 🚀 Load model at startup
model = load_model()


def ml_predict(features):
    try:
        # ❌ Model not loaded
        if model is None:
            print("⚠️ Model is None — fallback will be used")
            return None

        # 🔥 Prepare input safely
        X = [[
            float(features.get("close", 0)),
            float(features.get("ma_10", 0)),
            float(features.get("ma_50", 0)),
            float(features.get("volatility", 0))
        ]]

        # 🔥 Prediction
        pred = model.predict(X)[0]

        # 🔥 Convert to signal
        if pred == 1:
            return "BUY"
        else:
            return "SELL"

    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return None
