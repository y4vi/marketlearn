#!/usr/bin/env python3
# app.py
# Minimal dark-themed educational market analysis frontend

import streamlit as st
from data.market_data import fetch_market_data
from analysis.indicators import add_basic_indicators
from analysis.trends import describe_trend
from ai.ai.agent import agent
from utils.disclaimers import disclaimer
from visualization.charts import plot_price_and_indicators

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Market Learning Assistant",
    page_icon="📈",
    layout="centered"
)

# -----------------------------
# Dark minimal styling
# -----------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #0f1117;
        color: #e6e6e6;
    }
    .stTextInput > div > div > input {
        background-color: #1c1f26;
        color: white;
        border-radius: 10px;
    }
    .stButton button {
        background-color: #2d72ff;
        color: white;
        border-radius: 10px;
        padding: 0.6em 1.2em;
    }
    .stButton button:hover {
        background-color: #1b4fd6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Header
# -----------------------------
st.markdown("## 📊 Market Learning Assistant")
st.markdown(
    """
    Ask educational questions about the stock market.
    This tool explains trends, indicators, and context — **not financial advice**.
    """
)

# -----------------------------
# User input
# -----------------------------
col1, col2 = st.columns([3, 1])

with col1:
    ticker = st.text_input("Stock ticker", value="AAPL")

with col2:
    period = st.selectbox("Period", ["3mo", "6mo", "1y", "2y"], index=2)

question = st.text_input(
    "What would you like to understand?",
    placeholder="Explain the recent trend and indicators in simple terms"
)

# -----------------------------
# Run analysis
# -----------------------------
if st.button("Analyze"):
    try:
        with st.spinner("Analyzing market data..."):
            df = fetch_market_data(ticker)
            df = add_basic_indicators(df)
            trend = describe_trend(df)

        ai_response = agent.invoke({"input":
                f"""
                Stock: {ticker}
                Trend summary: {trend}
                User question: {question}
                Explain clearly for learning purposes.
                """
            })

        st.markdown("### 🧠 Explanation")
        st.write(ai_response.get("output", ai_response))

        st.markdown("### 📉 Price & Indicators")
        st.pyplot(plot_price_and_indicators(df))

        st.info(disclaimer())

    except Exception as e:
        st.error(str(e))
