from dash import Output, Input, html, dcc, callback_context
import dash
import plotly.express as px
from visuals.time_series import create_time_series_chart
import pandas as pd

def register_callbacks(app, time_series_df):

    @app.callback(
        Output("time-series-chart", "figure"),
        Input("stock-selector", "value"),
        Input("date-range-slider", "value")
    )
    def update_main_chart(selected_tickers, date_range):
        return create_time_series_chart(time_series_df, selected_tickers, date_range)


    @app.callback(
        Output("stock-concept-output", "children"),
        Input("stock-concept-dropdown", "value")
    )
    def update_stock_concept_info(concept):
        if concept is None:
            return ""

        components = []

        if concept == "volume":
            fig = px.line(
                time_series_df,
                x="Date",
                y="NVIDIA",
                title="NVIDIA Volume Over Time (Mocked)",
                labels={"NVIDIA": "Volume"}
            )

            components = [
                html.H5("Volume"),
                html.P("What it is: Volume measures how many shares were traded during a single trading day."),
                html.P(
                    "Why it matters: High volume indicates strong interest in the stock and can signal news, volatility, or institutional activity."),
                html.P(
                    "How to use it: Traders look for volume spikes to confirm a trend. For example, a breakout on high volume is more trustworthy than one on low volume."),
                html.Small("Fun Fact: NVIDIA’s trading volume jumped over 250% on its May 2023 earnings day."),
                dcc.Graph(figure=fig, config={"displayModeBar": False}, style={"height": "300px"})
            ]


        elif concept == "close":

            fig = px.line(

                time_series_df,

                x="Date",

                y="NVIDIA",

                title="NVIDIA Closing Price Over Time",

                labels={"NVIDIA": "Price (USD)"}

            )

            components = [
                html.H5("Closing Price"),
                html.P(
                    "What it is: The closing price is the last price a stock traded at during the regular trading session."),

                html.P(
                    "Why it matters: Closing price is the standard value used to track daily gains/losses and is often used in charts, financial media, and investment decisions."),

                html.P(
                    "How to use it: Investors compare a stock’s closing price to previous days to track trends or performance. It’s also used to calculate daily returns."),

                html.Small("Fun Fact: NVIDIA closed at an all-time high in November 2023."),

                dcc.Graph(figure=fig, config={"displayModeBar": False}, style={"height": "300px"})

            ]


        elif concept == "open":
            components = [
                html.H5("Opening Price"),
                html.P(
                    "What it is: The opening price is the first price at which a stock trades when the market opens at 9:30 AM EST."),
                html.P(
                    "Why it matters: It reflects overnight news and investor sentiment before market open. Large gaps from the previous close can indicate volatility."),
                html.P(
                    "How to use it: Compare the opening price to the previous close to gauge investor reaction to overnight events."),
                html.Small(
                    "Fun Fact: Stocks that ‘gap up’ at open often continue rising that day — if volume supports the move.")
            ]


        elif concept == "high":
            components = [
                html.H5("High Price"),
                html.P("What it is: The highest price the stock reached during the trading day."),
                html.P(
                    "Why it matters: It shows the upper bound of buying interest. Traders look at this to set resistance levels."),
                html.P("How to use it: Track the daily high to evaluate momentum and identify breakout attempts."),
                html.Small(
                    "Fun Fact: On May 24, 2023, NVIDIA hit a new intraday high — hours after releasing record-breaking AI earnings.")
            ]


        elif concept == "low":
            components = [
                html.H5("Low Price"),
                html.P("What it is: The lowest price the stock traded at during the day."),
                html.P("Why it matters: It helps assess the worst-case market sentiment during a trading session."),
                html.P(
                    "How to use it: Many investors use daily lows to set stop-loss levels or identify price support."),
                html.Small(
                    "Fun Fact: Stocks can dip sharply and recover in the same day — a phenomenon called a ‘hammer’ pattern.")
            ]


        elif concept == "adj_close":
            components = [
                html.H5("Adjusted Close"),
                html.P(
                    "What it is: Adjusted Close modifies the closing price to include dividends, stock splits, and other corporate actions."),
                html.P(
                    "Why it matters: It gives a more accurate reflection of a stock’s value over time — especially for long-term charts."),
                html.P(
                    "How to use it: Use adjusted close for historical comparisons and calculating true returns over time."),
                html.Small(
                    "Fun Fact: Without adjusted close, Apple’s 7-for-1 stock split would show a sudden crash on the chart!")
            ]


        elif concept == "earnings":

            components = [

                html.H5("Earnings"),

                html.P(
                    "What it is: Quarterly earnings are a company’s official report of profit/loss. They include revenue, expenses, and net income."),

                html.P(
                    "Why it matters: Earnings are the main indicator of a company’s financial health. Stocks often jump or drop after these reports."),

                html.P(
                    "How to use it: Watch earnings calendars. Price swings after earnings are common — especially if a company ‘beats’ or ‘misses’ analyst expectations."),

                html.Small("Fun Fact: NVIDIA’s stock jumped 24% in a single day after their record Q2 2023 earnings!")

            ]

        return components

    @app.callback(
        Output("nvda-price-chart", "figure"),
        Output("nvda-volume-chart", "figure"),
        Output("nvda-summary", "children"),
        Input("tabs", "active_tab"),
        Input("nvda-earnings-zoom", "value")
    )
    def update_nvda_tab(tab, selected_earnings_date):
        ctx = callback_context

        # Prevent unnecessary updates on first load
        if not ctx.triggered:
            return {}, {}, ""

        # Only update if we're on the NVIDIA tab
        if tab != "tab-nvda":
            raise dash.exceptions.PreventUpdate

        # Step 1: Get DataFrame + convert Date to datetime
        df = time_series_df.copy()
        df["Date"] = pd.to_datetime(df["Date"])
        df["Price"] = df["NVIDIA"]
        df["Volume"] = df["NVIDIA"] * 0.75e6  # Simulated volume

        # Step 2: Zoom to selected earnings date (if selected)
        if selected_earnings_date:
            selected_date = pd.to_datetime(selected_earnings_date)
            start = selected_date - pd.Timedelta(days=5)
            end = selected_date + pd.Timedelta(days=5)
            df = df[(df["Date"] >= start) & (df["Date"] <= end)]

        # Step 3: Price chart
        price_fig = px.line(df, x="Date", y="Price", title="NVIDIA Stock Price (Raw)",
                            labels={"Price": "Price (USD)"})
        price_fig.update_layout(template="plotly_white")

        # Step 4: Volume chart
        vol_fig = px.bar(df, x="Date", y="Volume", title="NVIDIA Volume (Simulated)",
                         labels={"Volume": "Volume"})
        vol_fig.update_layout(template="plotly_white")

        # Step 5: Yearly returns from full unfiltered data
        df_full = time_series_df.copy()
        df_full["Date"] = pd.to_datetime(df_full["Date"])

        pct_2023 = ((df_full[df_full["Date"].dt.year == 2023]["NVIDIA"].iloc[-1] -
                     df_full[df_full["Date"].dt.year == 2023]["NVIDIA"].iloc[0]) /
                    df_full[df_full["Date"].dt.year == 2023]["NVIDIA"].iloc[0]) * 100

        pct_2024 = ((df_full[df_full["Date"].dt.year == 2024]["NVIDIA"].iloc[-1] -
                     df_full[df_full["Date"].dt.year == 2024]["NVIDIA"].iloc[0]) /
                    df_full[df_full["Date"].dt.year == 2024]["NVIDIA"].iloc[0]) * 100

        summary = html.Div([
            html.H5("🧠 Why NVIDIA Matters"),
            html.P(f"📈 In 2023, NVIDIA gained **{pct_2023:.2f}%** — one of the best performers in the S&P 500."),
            html.P(f"⚡ In 2024 (so far), it has grown another **{pct_2024:.2f}%**."),
            html.P(
                "💬 With its dominance in AI chips, NVIDIA has become one of the most influential tech companies in the market."),
        ])

        return price_fig, vol_fig, summary


