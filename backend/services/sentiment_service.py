import requests

# 🔑 Your News API key
API_KEY = "82b27fbc0d82497bbdda05f5c66e9edd"


def get_sentiment(symbol="AAPL"):
    try:
        # 🔍 Fetch news related to the stock
        url = f"https://newsapi.org/v2/everything?q={symbol}&sortBy=publishedAt&apiKey={API_KEY}"

        response = requests.get(url, timeout=5)
        data = response.json()

        articles = data.get("articles", [])[:5]  # take top 5 news

        # 🔥 Simple keyword-based sentiment
        positive_words = ["growth", "profit", "gain", "up", "strong", "surge", "rise"]
        negative_words = ["loss", "drop", "down", "fall", "weak", "decline", "crash"]

        score = 0

        for article in articles:
            title = article.get("title", "").lower()

            for word in positive_words:
                if word in title:
                    score += 1

            for word in negative_words:
                if word in title:
                    score -= 1

        # 📊 Determine sentiment
        if score > 1:
            sentiment = "POSITIVE"
        elif score < -1:
            sentiment = "NEGATIVE"
        else:
            sentiment = "NEUTRAL"

        return {
            "score": score,
            "sentiment": sentiment
        }

    except Exception as e:
        print("❌ Sentiment error:", e)
        return {
            "score": 0,
            "sentiment": "NEUTRAL"
        }
