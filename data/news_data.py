import requests
from config.settings import NEWS_API_KEY
import os


def fetch_news(query: str, limit=5):
    url = "https://newsapi.org/v2/everything"
    api_key = NEWS_API_KEY or os.environ.get("NEWS_API_KEY")
    if not api_key:
        raise ValueError("NEWS_API_KEY is not set. Set NEWS_API_KEY in config/settings.py or environment variables.")

    params = {
        "q": query,
        "apiKey": api_key,
        "pageSize": limit,
        "sortBy": "relevancy"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json().get("articles", [])

# Summarize news for agent context
def fetch_news_context(query: str, limit=5):
    articles = fetch_news(query, limit)
    if not articles:
        return "No recent news found."
    summaries = []
    for article in articles:
        title = article.get("title", "")
        desc = article.get("description", "")
        source = article.get("source", {}).get("name", "")
        summaries.append(f"[{source}] {title}: {desc}")
    return "\n".join(summaries)