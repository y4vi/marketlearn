import matplotlib.pyplot as plt


def plot_price_and_indicators(df):
    """Return a matplotlib Figure plotting closing price and indicators.

    Returns the Figure so callers (e.g., Streamlit) can render it.
    """
    fig, ax = plt.subplots(figsize=(14, 7))

    if 'Close' in df.columns:
        ax.plot(df.index, df['Close'], label='Closing Price', color='blue')

    if 'SMA_20' in df.columns:
        ax.plot(df.index, df['SMA_20'], label='SMA 20', color='orange')

    if 'EMA_20' in df.columns:
        ax.plot(df.index, df['EMA_20'], label='EMA 20', color='green')

    ax.set_title('Price and Technical Indicators')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()

    return fig