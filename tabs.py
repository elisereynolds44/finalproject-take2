from dash import dcc, html
import pandas as pd
import dash_bootstrap_components as dbc
from visuals.time_series import create_time_series_chart, TICKER_TO_NAME
from visuals.heatmap import create_heatmap

months = pd.date_range(start="2023-01-01", end="2024-12-01", freq="MS")
month_labels = {i: date.strftime("%m.%y") for i, date in enumerate(months)}

def get_tabs(time_series_df, corr_matrix):
    try:
        heatmap_fig = create_heatmap(corr_matrix) if corr_matrix is not None else {}
    except Exception as e:
        print(f"⚠️ Error generating heatmap: {e}")
        heatmap_fig = {}

    return dbc.Tabs([

        dbc.Tab(label="📊 Price Trends", tab_id="tab-trends", children=[
            html.H4("Compare Stock Growth Over Time"),
            html.P("Normalized to 100, so you can see percentage-based growth between companies."),
            dcc.Dropdown(
                id='stock-selector',
                options=[{"label": TICKER_TO_NAME[t], "value": t} for t in TICKER_TO_NAME],
                value=["NVDA", "SPY", "QQQ"],  # ✅ Updated to match ETF tickers
                multi=True
            ),
            dcc.RangeSlider(
                id='date-range-slider',
                min=0,
                max=len(month_labels) - 1,
                step=1,
                marks=month_labels,
                value=[0, len(month_labels) - 1],
                tooltip={"placement": "bottom", "always_visible": True}
            ),

            dcc.Graph(id='time-series-chart')
        ]),

        dbc.Tab(label="📈 Correlation Matrix", tab_id="tab-correlation", children=[
            html.H4("How Closely Are These Stocks Moving Together?"),
            html.P("Correlation values show whether the stocks move in sync (1 = perfect correlation)."),
            dcc.Graph(figure=heatmap_fig)
        ]),

        dbc.Tab(label="💚 NVIDIA Focus", tab_id="tab-nvda", children=[
            html.H4("NVIDIA’s Market Trajectory"),

            html.Div([
                html.Label("Zoom to Earnings Date:"),
                dcc.Dropdown(
                    id="nvda-earnings-zoom",
                    options=[
                        {"label": "Feb 22, 2023", "value": "2023-02-22"},
                        {"label": "May 24, 2023", "value": "2023-05-24"},
                        {"label": "Aug 23, 2023", "value": "2023-08-23"},
                        {"label": "Nov 21, 2023", "value": "2023-11-21"},
                        {"label": "Feb 21, 2024", "value": "2024-02-21"},
                        {"label": "May 22, 2024", "value": "2024-05-22"}
                    ],
                    placeholder="Select an earnings date...",
                    style={"width": "50%", "marginBottom": "20px"}
                )
            ]),

            dcc.Graph(id="nvda-price-chart"),
            dcc.Graph(id="nvda-volume-chart"),

            html.Div(id="nvda-summary", style={"marginTop": "20px"})
        ]),

        dbc.Tab(label="🧠 Insights", tab_id="tab-insights", children=[
            html.H4("Key Takeaways from the Data"),
            html.Ul([
                html.Li("NVIDIA has grown over 1000% since early 2023, far outpacing the broader market."),
                html.Li("Competitors like AMD and Microsoft have shown solid growth, but nowhere near NVIDIA's scale."),
                html.Li("Intel has declined in value, making it a surprising outlier."),
                html.Li("NVIDIA’s stock is highly correlated with NASDAQ and S&P 500, reinforcing its leadership."),
                html.Li("Dell, HPE, and SuperMicro have also been lifted alongside NVIDIA’s growth.")
            ])
        ]),

        dbc.Tab(label="📘 Learn About Stocks", tab_id="tab-learn", children=[
            html.H4("Understand Key Stock Terms"),
            html.P("Select a concept to learn more about how stocks and markets work."),

            dcc.Dropdown(
                id="stock-concept-dropdown",
                options=[
                    {"label": "📈 Closing Price", "value": "close"},
                    {"label": "🛑 Opening Price", "value": "open"},
                    {"label": "📉 Lowest Price", "value": "low"},
                    {"label": "🚀 Highest Price", "value": "high"},
                    {"label": "🎛️ Adjusted Close", "value": "adj_close"},
                    {"label": "🔁 Volume", "value": "volume"},
                    {"label": "💼 Earnings", "value": "earnings"}
                ],
                placeholder="Select a concept...",
                style={"margin-bottom": "20px"}
            ),

            # ✅ This is where content will be displayed
            html.Div(id="stock-concept-output")
        ])

    ], id='tabs', active_tab='tab-trends')
