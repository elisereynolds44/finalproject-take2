import plotly.express as px
from datetime import datetime
import pandas as pd

# --- Color Map for Line Chart ---
color_discrete_map = {
    "NVIDIA": "green",
    "AMD": "red",
    "Intel": "gray",
    "S&P 500": "blue",
    "NASDAQ": "purple",
    "Microsoft": "orange",
    "Dell": "teal",
    "Hewlett Packard Enterprise": "brown",
    "SuperMicro": "pink"
}

# --- Ticker to Full Name ---
TICKER_TO_NAME = {
    "NVDA": "NVIDIA",
    "SPY": "S&P 500",
    "QQQ": "NASDAQ",
    "AMD": "AMD",
    "INTC": "Intel",
    "MSFT": "Microsoft",
    "DELL": "Dell",
    "HPE": "Hewlett Packard Enterprise",
    "SMCI": "SuperMicro"
}

def create_time_series_chart(df, selected_tickers, date_range=None):
    if df is None or df.empty or not selected_tickers:
        return px.line(
            title="No data available to display.",
            labels={"value": "Relative Price", "Date": "Date"}
        )

    df = df.copy()

    selected_columns = [TICKER_TO_NAME.get(t, t) for t in selected_tickers]
    existing_columns = [col for col in selected_columns if col in df.columns]

    if not existing_columns:
        return px.line(title="⚠️ Selected stocks not found in the data.")

    # Normalize to 100
    for col in df.columns:
        if col != "Date":
            df[col] = df[col] / df[col].iloc[0] * 100

    try:
        df_long = df[["Date"] + existing_columns].melt(
            id_vars="Date", var_name="Ticker", value_name="value"
        )
    except Exception as e:
        print(f"❌ Error melting DataFrame: {e}")
        return px.line(title="⚠️ Error rendering chart.")

    fig = px.line(
        df_long,
        x='Date',
        y='value',
        color='Ticker',
        title='Stock Comparison (Normalized to 100)',
        labels={"value": "Relative Price", "Ticker": "Company"},
        color_discrete_map=color_discrete_map
    )

    fig.update_layout(
        yaxis_title="Relative Growth (Starting at 100)",
        xaxis_title="Date",
        hovermode="x unified",
        template="plotly_white",
        legend_title="Company",
    )

    # Add earnings markers
    earnings_dates = [
        datetime(2023, 2, 22),
        datetime(2023, 5, 24),
        datetime(2023, 8, 23),
        datetime(2023, 11, 21),
        datetime(2024, 2, 21),
        datetime(2024, 5, 22)
    ]

    for date in earnings_dates:
        fig.add_vline(x=date, line_width=2, line_dash="dash", line_color="gray")
        fig.add_annotation(
            x=date,
            y=max(df_long["value"]),
            text="Earnings",
            showarrow=False,
            yshift=10,
            font=dict(size=10, color="gray")
        )

    # Zoom the x-axis based on month index
    if date_range:
        months = pd.date_range(start="2023-01-01", end="2024-12-01", freq="MS")
        start_date = months[date_range[0]]
        end_date = months[date_range[1]] + pd.offsets.MonthEnd(1)
        fig.update_xaxes(range=[start_date, end_date])

    return fig
