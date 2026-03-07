import yfinance as yf
import pandas as pd

def fetch_market_data(ticker: str, period: str = "1mo", interval: str = "1d") -> pd.DataFrame:
    """
    Fetch market data for a given ticker symbol.

    Args:
        ticker (str): The ticker symbol of the stock.
        period (str): The period for which to fetch data (default is "1mo").
        interval (str): The data interval (default is "1d").

    Returns:
        pd.DataFrame: A DataFrame containing the market data.
    """
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    return df