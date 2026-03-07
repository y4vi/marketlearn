#!/usr/bin/env python3

from data.market_data import fetch_market_data
from analysis.indicators import add_basic_indicators
from analysis.trends import describe_trend
from ai.ai.agent import agent

def get_disclaimer():
    return (
        "This analysis is for educational purposes only. "
        "It does not constitute financial advice. "
        "Market data can be incomplete or delayed."
    )

ticker = input("Enter stock ticker (default: AAPL): ").strip() or "AAPL"

df = fetch_market_data(ticker)
df = add_basic_indicators(df)

trend_description = describe_trend(df)

query = input("Enter your query for the AI agent: ").strip()

if not query:
    query = f"Stock Analysis for {ticker}: Trend Summary: {trend_description}. Explain this data clearly without giving financial advice or predictions."

response = agent.invoke({"input": query})

print("\n" + response.get("output", response))
print("\n" + get_disclaimer())