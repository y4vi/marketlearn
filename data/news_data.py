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