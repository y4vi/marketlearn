#!/usr/bin/env python3
# app.py — Educational market analysis chat interface
# Claude-inspired design with deep viridian green (#1d3a14) primary

import streamlit as st
import re
from data.market_data import fetch_market_data
from analysis.indicators import add_basic_indicators
from analysis.trends import describe_trend
from ai.ai.agent import agent
from utils.disclaimers import disclaimer
from visualization.charts import plot_price_and_indicators

# ── Page configuration ──
st.set_page_config(
    page_title="Market Learning Assistant",
    page_icon="📈",
    layout="centered",
)

# ── Claude-inspired styling with viridian green primary ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&family=DM+Serif+Display&family=JetBrains+Mono:wght@400&display=swap');

/* ── Global ── */
:root {
    --viridian: #1d3a14;
    --viridian-light: #2a5420;
    --viridian-lighter: #3a6e30;
    --bg-primary: #f4f2ef;
    --bg-secondary: #ebe8e3;
    --bg-elevated: #ffffff;
    --text-primary: #1a1814;
    --text-secondary: #6b6560;
    --text-placeholder: #a8a39d;
    --border: rgba(0,0,0,0.08);
    --border-strong: rgba(0,0,0,0.15);
    --accent-subtle: #d4e8cd;
}

.stApp {
    background-color: var(--bg-primary) !important;
    font-family: 'DM Sans', system-ui, sans-serif;
}

/* ── Header ── */
.app-header {
    text-align: center;
    padding: 2rem 1rem 1rem;
}
.app-header h1 {
    font-family: 'DM Serif Display', Georgia, serif;
    color: var(--viridian);
    font-size: 2rem;
    font-weight: 400;
    margin-bottom: 0.25rem;
}
.app-header p {
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.6;
    max-width: 520px;
    margin: 0 auto;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0.75rem 0 !important;
    max-width: 720px;
    margin: 0 auto;
    animation: messageIn 0.25s ease-out;
    color: #1d3a14 !important;
}

[data-testid="stChatMessage"] * {
    color: #1d3a14 !important;
}

@keyframes messageIn {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* User messages — subtle viridian tint */
[data-testid="stChatMessage"][data-testid-type="user"] .stMarkdown {
    background: var(--accent-subtle);
    border-radius: 16px 16px 4px 16px;
    padding: 12px 16px;
    color: #1d3a14 !important;
}
[data-testid="stChatMessage"][data-testid-type="user"] .stMarkdown p {
    color: #1d3a14 !important;
}

/* Assistant messages — clean prose, no bubble */
[data-testid="stChatMessage"][data-testid-type="assistant"] .stMarkdown {
    line-height: 1.75;
    color: #1d3a14 !important;
}
[data-testid="stChatMessage"][data-testid-type="assistant"] .stMarkdown p {
    color: #1d3a14 !important;
}

/* Force all markdown text to viridian */
.stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li, .stMarkdown h1,
.stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown strong, .stMarkdown em {
    color: #1d3a14 !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    max-width: 720px;
    margin: 0 auto;
}
[data-testid="stChatInput"] textarea {
    background: var(--bg-elevated) !important;
    border: 1.5px solid var(--border-strong) !important;
    border-radius: 16px !important;
    font-family: 'DM Sans', system-ui, sans-serif !important;
    font-size: 15px !important;
    padding: 12px 16px !important;
    color: #1d3a14 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--viridian) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 0 0 3px var(--accent-subtle) !important;
}
[data-testid="stChatInput"] button {
    background: var(--viridian) !important;
    color: white !important;
    border-radius: 12px !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
[data-testid="stChatInput"] button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
}

/* ── Info boxes ── */
.stAlert {
    background: var(--accent-subtle) !important;
    color: var(--viridian) !important;
    border-radius: 10px !important;
    border-left: 3px solid var(--viridian) !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: var(--viridian) !important;
}

/* ── Code blocks ── */
pre {
    background: #1c1917 !important;
    border-radius: 10px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}

/* ── Disclaimer bar ── */
.disclaimer-bar {
    text-align: center;
    font-size: 0.8rem;
    color: var(--text-secondary);
    padding: 1rem;
    border-top: 1px solid var(--border);
    margin-top: 1rem;
}

/* Hide Streamlit branding for clean look */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ── Header ──
st.markdown("""
<div class="app-header">
    <h1>Market Learning Assistant</h1>
    <p>Learn about the stock market through conversation.
    Ask about any publicly-listed company — the assistant will analyze data,
    create charts, and explain trends in context. Not financial advice.</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ──
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_ticker" not in st.session_state:
    st.session_state.last_ticker = None
if "last_df" not in st.session_state:
    st.session_state.last_df = None

# ── Helper: extract ticker from user message ──
def extract_ticker(text):
    """Try to extract a stock ticker from natural language."""
    # Match common patterns: $AAPL, AAPL, "ticker AAPL", etc.
    patterns = [
        r'\$([A-Z]{1,5})\b',           # $AAPL
        r'\b([A-Z]{1,5})\b',           # AAPL (uppercase 1-5 letters)
    ]
    # Common words to exclude
    exclude = {
        'I', 'A', 'AN', 'THE', 'AND', 'OR', 'BUT', 'FOR', 'NOT', 'IS',
        'IT', 'TO', 'IN', 'ON', 'AT', 'BY', 'OF', 'IF', 'SO', 'DO',
        'UP', 'NO', 'AS', 'AM', 'BE', 'HE', 'WE', 'MY', 'ME', 'US',
        'AI', 'OK', 'VS', 'RE', 'EMA', 'SMA', 'RSI', 'CEO', 'IPO',
        'GDP', 'ETF', 'HOW', 'WHY', 'CAN', 'HAS', 'HAD', 'WAS', 'ARE',
        'HIS', 'HER', 'ITS', 'ALL', 'ANY', 'FEW', 'NEW', 'OLD', 'OUR',
        'OWN', 'SAY', 'SHE', 'TOO', 'USE', 'WAY', 'WHO', 'DAY', 'GET',
        'HIM', 'MAY', 'OUT', 'PUT', 'RUN', 'SET', 'TRY', 'TWO', 'YET',
    }
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            if m not in exclude and len(m) >= 2:
                return m
    return None

# ── Display conversation history ──
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("chart"):
            st.pyplot(message["chart"])

# ── Chat input ──
if prompt := st.chat_input("Ask about any stock — e.g. 'Tell me about Tesla's recent performance'"):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Extract ticker from message (or reuse last one)
    ticker = extract_ticker(prompt)
    if not ticker and st.session_state.last_ticker:
        ticker = st.session_state.last_ticker

    # Fetch market data if we have a ticker
    df = None
    trend = ""
    chart_fig = None
    if ticker:
        try:
            with st.spinner("Fetching market data..."):
                df = fetch_market_data(ticker, period="1y")
                df = add_basic_indicators(df)
                trend = describe_trend(df)
                chart_fig = plot_price_and_indicators(df, ticker)
            st.session_state.last_ticker = ticker
            st.session_state.last_df = df
        except Exception:
            trend = f"Could not fetch data for ticker '{ticker}'."

    # Build agent input
    agent_input = prompt
    if ticker and trend:
        agent_input = f"Stock: {ticker}\nTrend summary: {trend}\nUser message: {prompt}"

    # Build conversation history for context
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[:-1]  # exclude current message
    ]

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ai_response = agent.invoke({
                "input": agent_input,
                "history": history,
                "ticker": ticker or "",
            })
        response_text = ai_response.get("output", str(ai_response))
        st.markdown(response_text)

        # Show chart if we have data
        if chart_fig:
            st.pyplot(chart_fig)

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "chart": chart_fig,
    })

    # Disclaimer
    st.markdown(f'<div class="disclaimer-bar">{disclaimer()}</div>', unsafe_allow_html=True)
