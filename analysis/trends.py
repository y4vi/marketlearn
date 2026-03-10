import pandas as pd


def describe_trend(df):
    """Generate a detailed statistical summary of the stock's performance."""
    if df is None or df.empty:
        return "No data available to describe trend."

    try:
        close = df['Close'].dropna()
    except Exception:
        return "Data does not contain 'Close' prices."

    if len(close) < 2:
        return "Not enough data to determine trend."

    parts = []

    # Price range and current
    current_price = close.iloc[-1]
    start_price = close.iloc[0]
    high = close.max()
    low = close.min()
    total_change = ((current_price - start_price) / start_price) * 100
    parts.append(f"Current price: ${current_price:.2f}")
    parts.append(f"Period start price: ${start_price:.2f}")
    parts.append(f"Period change: {total_change:+.2f}%")
    parts.append(f"Period high: ${high:.2f}, Period low: ${low:.2f}")

    # Recent performance (last 20 days)
    n = min(20, len(close))
    recent = close[-n:]
    recent_change = ((recent.iloc[-1] - recent.iloc[0]) / recent.iloc[0]) * 100
    parts.append(f"Last {n} days change: {recent_change:+.2f}%")

    # Moving averages
    if 'SMA_20' in df.columns and not df['SMA_20'].dropna().empty:
        sma = df['SMA_20'].dropna().iloc[-1]
        sma_vs = ((current_price - sma) / sma) * 100
        parts.append(f"SMA 20: ${sma:.2f} (price is {sma_vs:+.2f}% vs SMA)")

    if 'EMA_20' in df.columns and not df['EMA_20'].dropna().empty:
        ema = df['EMA_20'].dropna().iloc[-1]
        ema_vs = ((current_price - ema) / ema) * 100
        parts.append(f"EMA 20: ${ema:.2f} (price is {ema_vs:+.2f}% vs EMA)")

    # RSI
    if 'RSI_14' in df.columns and not df['RSI_14'].dropna().empty:
        rsi = df['RSI_14'].dropna().iloc[-1]
        rsi_label = "overbought" if rsi > 70 else "oversold" if rsi < 30 else "neutral"
        parts.append(f"RSI 14: {rsi:.1f} ({rsi_label})")

    # Volume
    if 'Volume' in df.columns and not df['Volume'].dropna().empty:
        avg_vol = df['Volume'].mean()
        recent_vol = df['Volume'].iloc[-5:].mean()
        parts.append(f"Avg volume: {avg_vol:,.0f}, Recent 5-day avg: {recent_vol:,.0f}")

    # Volatility (std of daily returns)
    daily_returns = close.pct_change().dropna()
    if len(daily_returns) > 1:
        volatility = daily_returns.std() * 100
        parts.append(f"Daily volatility: {volatility:.2f}%")

    # Trend direction
    ma_short = recent.rolling(window=5, min_periods=1).mean().iloc[-1]
    ma_long = recent.rolling(window=min(20, len(recent)), min_periods=1).mean().iloc[-1]
    if ma_short > ma_long:
        parts.append("Trend signal: short MA above long MA (bullish)")
    elif ma_short < ma_long:
        parts.append("Trend signal: short MA below long MA (bearish)")
    else:
        parts.append("Trend signal: neutral")

    return "\n".join(parts)

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