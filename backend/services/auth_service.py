users_db = {}  # temporary storage


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

    return {
        "message": "Login successful",
        "token": f"{username}_token"
    }
