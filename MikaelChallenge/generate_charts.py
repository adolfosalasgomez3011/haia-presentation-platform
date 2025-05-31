
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
import os

def generate_charts(symbol="SXC", output_dir="img"):
    os.makedirs(output_dir, exist_ok=True)
    stock = yf.Ticker(symbol)

    # 1. Historical Price Chart (1 year)
    hist = stock.history(period="1y")
    plt.figure(figsize=(10, 4))
    plt.plot(hist.index, hist["Close"], label="Close Price", color="blue")
    plt.title(f"{symbol} - 1 Year Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{symbol.lower()}_price_1y.png"))
    plt.close()

    # 2. Revenue Bar Chart (last 4 periods if available)
    try:
        income_stmt = stock.financials
        revenue_series = income_stmt.loc["Total Revenue"]
        if not revenue_series.empty:
            plt.figure(figsize=(6, 4))
            revenue_series = revenue_series / 1e9  # convert to billions
            revenue_series.plot(kind="bar", color="green")
            plt.title(f"{symbol} - Quarterly Revenue (Billion USD)")
            plt.ylabel("Revenue (B)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"{symbol.lower()}_revenue_bars.png"))
            plt.close()
    except Exception as e:
        print("⚠️ Revenue data not available or could not be plotted:", e)

    # 3. Candlestick Chart (3 months)
    try:
        hist_candle = stock.history(period="3mo")
        mpf.plot(
            hist_candle,
            type="candle",
            style="yahoo",
            title=f"{symbol} - 3 Month Candlestick",
            ylabel="Price (USD)",
            volume=True,
            mav=(3, 6),
            savefig=os.path.join(output_dir, f"{symbol.lower()}_candlestick.png")
        )
    except Exception as e:
        print("⚠️ Candlestick chart could not be plotted:", e)

    print("✅ Charts saved to 'img/' folder.")

if __name__ == "__main__":
    generate_charts()
