import pandas as pd

def rsi(series, period=14):
    """
    Calculate RSI for a pandas Series.
    """
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def add_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add basic technical indicators to the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing market data with 'Close' prices.

    Returns:
        pd.DataFrame: DataFrame with added technical indicators.
    """
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['EMA_20'] = df['Close'].ewm(span=20).mean()
    df['RSI_14'] = rsi(df['Close'], period=14)
    return df