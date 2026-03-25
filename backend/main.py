from fastapi import FastAPI
from backend.services.data_service import get_stock_data
from backend.services.feature_service import get_features
from backend.services.prediction_service import predict_signal
app = FastAPI()

@app.get("/")
def home():
    return {"message": "QuantEdge AI – PN Labs API Running 🚀"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "system": "QuantEdge AI",
        "version": "v1"
    }

@app.get("/stock/{symbol}")
def stock(symbol: str):
    return get_stock_data(symbol)
@app.get("/features/{symbol}")
def features(symbol: str):
    return get_features(symbol)
@app.get("/predict/{symbol}")
def predict(symbol: str):
    return predict_signal(symbol)
