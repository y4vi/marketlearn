import talib
import pandas as pd

def add_basic_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add basic technical indicators to the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing market data with 'Close' prices.

    Returns:
        pd.DataFrame: DataFrame with added technical indicators.
    """
    df['SMA_20'] = talib.SMA(df['Close'], timeperiod=20)
    df['EMA_20'] = talib.EMA(df['Close'], timeperiod=20)
    df['RSI_14'] = talib.RSI(df['Close'], timeperiod=14)
    return df