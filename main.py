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

df = fetch_market_data(ticker, period="1y")
df = add_basic_indicators(df)

trend_description = describe_trend(df)

print("\nYou can ask follow-up questions. Type 'quit' to exit.\n")

history = []
while True:
    query = input("You: ").strip()
    if query.lower() in ('quit', 'exit', 'q'):
        break
    if not query:
        continue

    agent_input = f"Stock: {ticker}\nTrend summary: {trend_description}\nUser message: {query}"

    response = agent.invoke({
        "input": agent_input,
        "history": history,
        "ticker": ticker,
    })

    output = response.get("output", str(response))
    print(f"\nAssistant: {output}\n")

    history.append({"role": "user", "content": query})
    history.append({"role": "assistant", "content": output})

print("\n" + get_disclaimer())