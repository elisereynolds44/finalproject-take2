import pandas as pd
import os

# Load precomputed time series data
def prepare_time_series(_=None):
    path = "time_series_backup.csv"
    if os.path.exists(path):
        return pd.read_csv(path, parse_dates=["Date"])
    else:
        print("❌ Missing time_series_backup.csv")
        return None

# Load precomputed correlation matrix
def prepare_correlation_matrix(_=None):
    path = "correlation_matrix.csv"
    if os.path.exists(path):
        return pd.read_csv(path, index_col=0)
    else:
        print("❌ Missing correlation_matrix.csv")
        return None
