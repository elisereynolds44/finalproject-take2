import plotly.express as px
from datetime import datetime

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
    "^GSPC": "S&P 500",
    "^IXIC": "NASDAQ",
    "AMD": "AMD",
    "INTC": "Intel",
    "MSFT": "Microsoft",
    "DELL": "Dell",
    "HPE": "Hewlett Packard Enterprise",
    "SMCI": "SuperMicro"
}


# --- Create Line Chart ---
def create_time_series_chart(df, selected_tickers):
    if df is None or df.empty or not selected_tickers:
        return px.line(
            title="No data available to display.",
            labels={"value": "Relative Price", "Date": "Date"}
        )

    # Map to company names
    selected_columns = [TICKER_TO_NAME.get(t, t) for t in selected_tickers]
    existing_columns = [col for col in selected_columns if col in df.columns]

    if not existing_columns:
        return px.line(title="⚠️ Selected stocks not found in the data.")

    try:
        df_long = df[["Date"] + existing_columns].melt(
            id_vars="Date", var_name="Ticker", value_name="value"
        )
    except Exception as e:
        print(f"❌ Error melting DataFrame: {e}")
        return px.line(title="⚠️ Error rendering chart.")

    # Create the chart
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

    # --- Add Earnings Markers ---
    earnings_dates = [
        datetime(2023, 2, 22),
        datetime(2023, 5, 24),
        datetime(2023, 8, 23),
        datetime(2023, 11, 21),
        datetime(2024, 2, 21),
        datetime(2024, 5, 22)
    ]

    for date in earnings_dates:
        fig.add_vline(
            x=date,
            line_width=2,
            line_dash="dash",
            line_color="gray",
            annotation_text="Earnings",
            annotation_position="top left",
            annotation_font_size=10
        )

    return fig
