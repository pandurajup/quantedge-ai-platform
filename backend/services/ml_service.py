import pickle
import os

# Model path (important)
MODEL_PATH = "ml_models/model.pkl"

def load_model():
    try:
        if os.path.exists(MODEL_PATH):
            print(f"✅ Model file found at: {MODEL_PATH}")
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)
                print("✅ Model loaded successfully")
                return model
        else:
            print(f"❌ Model file NOT found at: {MODEL_PATH}")
            return None
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None

# Load model at startup
model = load_model()

def ml_predict(features):
    try:
        if model is None:
            print("⚠️ Model is not loaded, using fallback")
            return None

        # Prepare input features
        X = [[
            float(features["close"]),
            float(features["ma_10"]),
            float(features["ma_50"]),
            float(features["volatility"])
        ]]

        # Make prediction
        pred = model.predict(X)[0]

        # Convert to signal
        if pred == 1:
            return "BUY"
        else:
            return "SELL"

    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return None
