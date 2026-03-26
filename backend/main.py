from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
from backend.database import create_users_table
from backend.services.auth_service import signup, login
from backend.services.data_service import get_stock_data, get_chart_data
from backend.services.feature_service import get_features
from backend.services.prediction_service import
from backend.database import create_trades_table(
    predict_signal,
    get_top_picks,
    get_portfolio
)

# 🔐 JWT Config
SECRET_KEY = "quantedge_secret"
ALGORITHM = "HS256"

# 🚀 Initialize app
app = FastAPI()
create_users_table()
create_trades_table()
# 🔥 Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔐 Token verification
def verify_token(authorization: str = Header(None)):
    try:
        if not authorization:
            return None

        token = authorization.split(" ")[1]  # Bearer <token>
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return None


# 🏠 Home
@app.get("/")
def home():
    return {"message": "QuantEdge AI – PN Labs API Running 🚀"}


# ❤️ Health
@app.get("/health")
def health():
    return {
        "status": "ok",
        "system": "QuantEdge AI",
        "version": "v1"
    }


# 🔐 AUTH APIs
@app.post("/signup")
def signup_api(data: dict):
    return signup(data["username"], data["password"])


@app.post("/login")
def login_api(data: dict):
    return login(data["username"], data["password"])


# 📊 Raw stock data (public)
@app.get("/stock/{symbol}")
def stock(symbol: str):
    return get_stock_data(symbol)


# 🧠 Features (public)
@app.get("/features/{symbol}")
def features(symbol: str):
    return get_features(symbol)


# 📈 Chart (public)
@app.get("/chart/{symbol}")
def chart(symbol: str):
    return get_chart_data(symbol)


# 🎯 AI Prediction (PROTECTED)
@app.get("/predict/{symbol}")
def predict(symbol: str, user=verify_token()):
    if not user:
        return {"error": "Unauthorized"}
    return predict_signal(symbol)


# ⭐ Top Picks (PROTECTED)
@app.get("/top-picks")
def top_picks(user=verify_token()):
    if not user:
        return {"error": "Unauthorized"}
    return get_top_picks()


# 💰 Portfolio (PROTECTED)
@app.get("/portfolio")
def portfolio(user=verify_token()):
    if not user:
        return {"error": "Unauthorized"}
    return get_portfolio()
