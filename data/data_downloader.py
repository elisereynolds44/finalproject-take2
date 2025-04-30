import yfinance as yf
import pandas as pd
import time
import os

# --- Ticker & Label Setup ---
TICKERS = {
    "NVDA": "NVIDIA",
    "^GSPC": "S&P 500",
    "^IXIC": "NASDAQ",
    "AMD": "AMD",
    "INTC": "Intel",
    "MSFT": "Microsoft",
    "DELL": "Dell",
    "HPE": "Hewlett Packard Enterprise",
    "SMCI": "SuperMicro"
}


# --- Download Stock Data (Per-Ticker with Retry) ---
def get_stock_data():
    data = {}
    for ticker in TICKERS:
        success = False
        attempts = 0
        while not success and attempts < 5:
            try:
                print(f"Downloading {ticker}...")
                df = yf.download(ticker, start="2023-01-01", end="2024-12-31", auto_adjust=True, progress=False)
                if not df.empty:
                    data[ticker] = df
                    success = True
                else:
                    print(f"{ticker} returned empty data.")
            except Exception as e:
                print(f"Error downloading {ticker}: {e}. Retrying...")
                attempts += 1
                time.sleep(1.5)
    return data


# --- Prepare Time Series Data (Normalized + Backup) ---
def prepare_time_series(data):
    backup_path = "time_series_backup.csv"

    try:
        df = pd.concat(
            [data[ticker]["Close"].rename(name) for ticker, name in TICKERS.items()],
            axis=1
        ).dropna()

        if df.empty:
            raise ValueError("DataFrame is empty after merging stock data.")

        df = df / df.iloc[0] * 100
        df = df.reset_index()
        df["Date"] = pd.to_datetime(df["Date"])

        # Save backup
        df.to_csv(backup_path, index=False)
        print(f"✅ Time series data saved to {backup_path}")
        return df

    except Exception as e:
        print(f"⚠️ Error preparing time series: {e}")
        # Try fallback
        if os.path.exists(backup_path):
            print("🔁 Loading backup CSV instead...")
            return pd.read_csv(backup_path, parse_dates=["Date"])
        else:
            print("❌ No backup file found either.")
            return None


# --- Prepare Correlation Matrix ---
def prepare_correlation_matrix(data):
    try:
        close_prices = pd.DataFrame({
            ticker: data[ticker]["Close"] for ticker in TICKERS
        }).dropna()
        return close_prices.corr()
    except Exception as e:
        print(f"Error preparing correlation matrix: {e}")
        return None
