from backend.database import get_connection


# 💾 Save trade
def save_trade(username, symbol, action, price):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO trades (username, symbol, action, price) VALUES (?, ?, ?, ?)",
        (username, symbol, action, price)
    )

    conn.commit()
    conn.close()

    return {"message": "Trade saved successfully"}


# 📊 Get user trades
def get_user_trades(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT symbol, action, price, date FROM trades WHERE username=? ORDER BY date DESC",
        (username,)
    )

    rows = cursor.fetchall()
    conn.close()

    trades = []
    for r in rows:
        trades.append({
            "symbol": r[0],
            "action": r[1],
            "price": r[2],
            "date": r[3]
        })

    return {"trades": trades}
