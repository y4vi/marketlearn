# Market Learning Assistant

An educational Python application for learning about stock market analysis through interactive exploration of market data, technical indicators, and AI-powered explanations. This tool is designed for educational purposes only and does not provide financial advice or investment recommendations.

## Features

- **Market Data Fetching**: Retrieve historical stock data using Yahoo Finance
- **Technical Indicators**: Calculate and visualize basic indicators like moving averages, RSI, and MACD
- **Trend Analysis**: Automatic trend detection and description
- **AI-Powered Explanations**: Use OpenAI's GPT models to answer questions about market data and indicators
- **Interactive Web Interface**: Streamlit-based UI for easy exploration
- **Command-Line Interface**: Simple CLI version for quick analysis

## Technology Stack

- **Backend**: Python 3.9+
- **Data**: yfinance, pandas, numpy
- **AI**: OpenAI API
- **Visualization**: Matplotlib
- **Web UI**: Streamlit
- **Environment**: python-dotenv for configuration

## Important Disclaimer

This application is for educational and learning purposes only. All analysis and explanations are provided for informational purposes and should not be considered as financial advice, investment recommendations, or trading signals. Market data may be delayed or incomplete. Always consult with qualified financial professionals before making investment decisions.

# Market Learning Assistant — Run Instructions

Quick steps to run the project on macOS.

1) Create and activate a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

2) Install Python dependencies

```bash
pip install -r requirements.txt
```

4) Provide API keys

- Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY` (and `NEWS_API_KEY` if used).

```bash
cp .env.example .env
# edit .env and set OPENAI_API_KEY=sk-...
```

5) Run the CLI (prompt-driven)

```bash
python main.py
```

6) Or run the Streamlit web UI

```bash
streamlit run app.py
```

Troubleshooting

- If the agent raises an error about `OPENAI_API_KEY`, set the env variable or place it in `.env`.

Files of interest: `main.py`, `app.py`, `config/settings.py`, `ai/ai/agent.py`.

If you want, I can: (A) create the `.venv` and install dependencies here, (B) run the app once dependencies are present, or (C) inspect and update `ai/ai/agent.py` to support other LLM configs.
