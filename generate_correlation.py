import pandas as pd

# Load the final time series CSV
df = pd.read_csv("time_series_backup.csv")

# Drop the Date column
df_corr = df.drop(columns=["Date"]).corr()

# Save it as a new CSV
df_corr.to_csv("correlation_matrix.csv")
print("✅ Saved correlation_matrix.csv")
