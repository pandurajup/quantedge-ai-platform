from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.services.data_service import get_stock_data
from backend.services.feature_service import get_features
from backend.services.prediction_service import predict_signal, get_top_picks

# 🚀 Initialize app
app = FastAPI()

# 🔥 Enable CORS (VERY IMPORTANT for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains (can restrict later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🏠 Home route
@app.get("/")
def home():
    return {"message": "QuantEdge AI – PN Labs API Running 🚀"}

# ❤️ Health check
@app.get("/health")
def health():
    return {
        "status": "ok",
        "system": "QuantEdge AI",
        "version": "v1"
    }

# 📊 Raw stock data
@app.get("/stock/{symbol}")
def stock(symbol: str):
    return get_stock_data(symbol)

# 🧠 Feature engineering output
@app.get("/features/{symbol}")
def features(symbol: str):
    return get_features(symbol)

# 🎯 AI Prediction
@app.get("/predict/{symbol}")
def predict(symbol: str):
    return predict_signal(symbol)

# ⭐ NEW — Top AI Picks
@app.get("/top-picks")
def top_picks():
    return get_top_picks()
