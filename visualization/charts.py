import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'sans-serif'


def plot_price_and_indicators(df, ticker=""):
    """Return a matplotlib Figure with warm viridian-themed chart."""
    viridian = '#1d3a14'
    viridian_light = '#2a5420'
    warm_bg = '#f4f2ef'
    warm_card = '#faf9f7'
    text_color = '#1a1814'
    text_muted = '#6b6560'

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), height_ratios=[3, 1],
                                    gridspec_kw={'hspace': 0.3})

    title = f'{ticker} — Price & Indicators' if ticker else 'Price & Indicators'
    fig.suptitle(title, fontsize=16, fontweight='bold', color=text_color, y=0.97)
    fig.patch.set_facecolor(warm_bg)

    # Price chart
    ax1.set_facecolor(warm_card)
    if 'Close' in df.columns:
        ax1.plot(df.index, df['Close'], label='Close', color=viridian, linewidth=2.2)
    if 'SMA_20' in df.columns:
        ax1.plot(df.index, df['SMA_20'], label='SMA 20', color='#cc7e3a',
                 linestyle='--', linewidth=1.2, alpha=0.8)
    if 'EMA_20' in df.columns:
        ax1.plot(df.index, df['EMA_20'], label='EMA 20', color=viridian_light,
                 linestyle='-.', linewidth=1.2, alpha=0.8)

    ax1.set_ylabel('Price ($)', color=text_color, fontsize=11)
    ax1.legend(fontsize=9, framealpha=0.7, loc='upper left')
    ax1.grid(True, alpha=0.12, color='#000')
    ax1.tick_params(colors=text_muted, labelsize=9)
    for spine in ax1.spines.values():
        spine.set_color('#e0ddd8')

    # RSI chart
    ax2.set_facecolor(warm_card)
    if 'RSI_14' in df.columns:
        ax2.plot(df.index, df['RSI_14'], color=viridian, linewidth=1.5)
        ax2.axhline(70, color='#cc7e3a', linestyle='--', alpha=0.5, linewidth=0.8)
        ax2.axhline(30, color=viridian_light, linestyle='--', alpha=0.5, linewidth=0.8)
        ax2.fill_between(df.index, 30, 70, alpha=0.04, color=viridian)
        ax2.set_ylim(0, 100)

    ax2.set_ylabel('RSI', color=text_color, fontsize=11)
    ax2.set_xlabel('Date', color=text_color, fontsize=11)
    ax2.grid(True, alpha=0.12, color='#000')
    ax2.tick_params(colors=text_muted, labelsize=9)
    for spine in ax2.spines.values():
        spine.set_color('#e0ddd8')

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    return fig