from jose import jwt
from datetime import datetime, timedelta
from backend.database import get_connection

SECRET_KEY = "quantedge_secret"
ALGORITHM = "HS256"


def create_token(username):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=5)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def signup(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return {"message": "User created successfully"}

    except:
        return {"error": "User already exists"}

    finally:
        conn.close()


def login(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        return {"error": "Invalid username or password"}

    token = create_token(username)

    return {
        "message": "Login successful",
        "token": token
    }
