from backend.database import get_connection


def create_alert(username, symbol, message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO alerts (username, symbol, message) VALUES (?, ?, ?)",
        (username, symbol, message)
    )

    conn.commit()
    conn.close()


def get_alerts(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT symbol, message, date FROM alerts WHERE username=? ORDER BY date DESC",
        (username,)
    )

    rows = cursor.fetchall()
    conn.close()

    alerts = []
    for r in rows:
        alerts.append({
            "symbol": r[0],
            "message": r[1],
            "date": r[2]
        })

    return {"alerts": alerts}
