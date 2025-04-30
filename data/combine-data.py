import pandas as pd

# Map tickers to (file2023, file2024, Label for dashboard)
files = {
    "NVDA": ("NVDA-2023.csv", "NVDA-2024.csv", "NVIDIA"),
    "AMD": ("AMD-2023.csv", "AMD-2024.csv", "AMD"),
    "INTC": ("INTC-2023.csv", "INTC-2024.csv", "Intel"),
    "MSFT": ("MSFT-2023.csv", "MSFT-2024.csv", "Microsoft"),
    "SPY": ("SPY-2023.csv", "SPY-2024.csv", "S&P 500"),
    "QQQ": ("QQQ-2023.csv", "QQQ-2024.csv", "NASDAQ"),
    "DELL": ("DELL-2023.csv", "DELL-2024.csv", "Dell"),
    "HPE": ("HPE-2023.csv", "HPE-2024.csv", "Hewlett Packard Enterprise"),
    "SMCI": ("SMCI-2023.csv", "SMCI-2024.csv", "SuperMicro")
}

final_df = None

for ticker, (file_2023, file_2024, label) in files.items():
    try:
        df1 = pd.read_csv(file_2023, parse_dates=["Date"])
        df2 = pd.read_csv(file_2024, parse_dates=["Date"])
        df = pd.concat([df1, df2])
        df = df[["Date", "Adj Close"]].rename(columns={"Adj Close": label})
        df = df.sort_values("Date")

        if final_df is None:
            final_df = df
        else:
            final_df = pd.merge(final_df, df, on="Date", how="outer")
    except Exception as e:
        print(f"⚠️ Error processing {ticker}: {e}")

if final_df is not None:
    final_df = final_df.dropna().sort_values("Date")
    for col in final_df.columns:
        if col != "Date":
            final_df[col] = final_df[col] / final_df[col].iloc[0] * 100
    final_df.to_csv("../time_series_backup.csv", index=False)
    print("✅ Combined and saved to time_series_backup.csv")
else:
    print("❌ No data was combined. Check file names.")

# Normalize
for col in final_df.columns:
    if col != "Date":
        final_df[col] = final_df[col] / final_df[col].iloc[0] * 100

final_df.to_csv("time_series_backup.csv", index=False)
print("✅ Combined and saved to time_series_backup.csv")
