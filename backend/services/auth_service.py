from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "quantedge_secret"
ALGORITHM = "HS256"

users_db = {}


def create_token(username):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=5)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def signup(username, password):
    if username in users_db:
        return {"error": "User already exists"}

    users_db[username] = password
    return {"message": "User created successfully"}


def login(username, password):
    if username not in users_db:
        return {"error": "User not found"}

    if users_db[username] != password:
        return {"error": "Invalid password"}

    token = create_token(username)

    return {
        "message": "Login successful",
        "token": token
    }
