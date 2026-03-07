import pandas as pd


def describe_trend(df):
    """
    Placeholder function for describing trends.
    """
    if df is None or df.empty:
        return "No data available to describe trend."

    # Use simple signals: recent slope, SMA vs price
    try:
        close = df['Close'].dropna()
    except Exception:
        return "Data does not contain 'Close' prices."

    if len(close) < 2:
        return "Not enough data to determine trend."

    # recent slope (linear fit on last N points)
    n = min(20, len(close))
    recent = close[-n:]
    x = list(range(len(recent)))
    # linear slope (simple) — use differencing
    slope = (recent.iloc[-1] - recent.iloc[0]) / max(1, len(recent)-1)

    ma_short = recent.rolling(window=5, min_periods=1).mean().iloc[-1]
    ma_long = recent.rolling(window=20, min_periods=1).mean().iloc[-1]

    parts = []
    if slope > 0:
        parts.append("short-term upward slope")
    elif slope < 0:
        parts.append("short-term downward slope")
    else:
        parts.append("stable short-term price")

    if ma_short > ma_long:
        parts.append("short MA is above long MA (bullish signal)")
    elif ma_short < ma_long:
        parts.append("short MA is below long MA (bearish signal)")

    return ", ".join(parts)

class TrendAnalyzer:
    """
    A class to analyze trends in market data.
    """

    def __init__(self, df):
        """
        Initialize the TrendAnalyzer with market data.

        Args:
            df (pd.DataFrame): DataFrame containing market data with 'Close' prices.
        """
        self.df = df

    def moving_average_trend(self, window: int = 20) -> pd.Series:
        """
        Calculate the moving average trend.

        Args:
            window (int): The window size for the moving average (default is 20).

        Returns:
            pd.Series: A Series representing the moving average trend.
        """
        return self.df['Close'].rolling(window=window).mean()

    def price_trend(self) -> pd.Series:
        """
        Determine the price trend based on closing prices.

        Returns:
            pd.Series: A Series indicating the price trend direction.
        """
        trend = self.df['Close'].diff()
        trend_direction = trend.apply(lambda x: 'up' if x > 0 else ('down' if x < 0 else 'stable'))
        return trend_direction