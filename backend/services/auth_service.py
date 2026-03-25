import bcrypt
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


# 🔐 HASH PASSWORD
def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


# 🔐 VERIFY PASSWORD
def verify_password(password: str, hashed: bytes):
    return bcrypt.checkpw(password.encode(), hashed)


def signup(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        hashed = hash_password(password)

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed)
        )
        conn.commit()

        return {"message": "User created securely"}

    except:
        return {"error": "User already exists"}

    finally:
        conn.close()


def login(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "User not found"}

    stored_password = row[0]

    # 🔐 Verify hashed password
    if not verify_password(password, stored_password):
        return {"error": "Invalid password"}

    token = create_token(username)

    return {
        "message": "Login successful",
        "token": token
    }
