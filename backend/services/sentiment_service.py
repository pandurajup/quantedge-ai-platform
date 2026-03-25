import random

def get_sentiment(symbol="AAPL"):
    try:
        # 🔥 TEMP (simulate sentiment)
        # Later we will connect real news APIs

        sentiment_score = random.uniform(-1, 1)

        if sentiment_score > 0.2:
            sentiment = "POSITIVE"
        elif sentiment_score < -0.2:
            sentiment = "NEGATIVE"
        else:
            sentiment = "NEUTRAL"

        return {
            "score": sentiment_score,
            "sentiment": sentiment
        }

    except Exception as e:
        return {"error": str(e)}
