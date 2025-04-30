from dash import dcc, html
import dash_bootstrap_components as dbc
from visuals.time_series import create_time_series_chart, TICKER_TO_NAME
from visuals.heatmap import create_heatmap

def get_tabs(time_series_df, corr_matrix):
    return dbc.Tabs([

        dbc.Tab(label="📊 Price Trends", tab_id="tab-trends", children=[
            html.H4("Compare Stock Growth Over Time"),
            html.P("Normalized to 100, so you can see percentage-based growth between companies."),
            dcc.Dropdown(
                id='stock-selector',
                options=[{"label": TICKER_TO_NAME[t], "value": t} for t in TICKER_TO_NAME],
                value=["NVDA", "^GSPC", "^IXIC"],  # Default starting view
                multi=True
            ),
            dcc.Graph(id='time-series-chart')
        ]),

        dbc.Tab(label="📈 Correlation Matrix", tab_id="tab-correlation", children=[
            html.H4("How Closely Are These Stocks Moving Together?"),
            html.P("Correlation values show whether the stocks move in sync (1 = perfect correlation)."),
            dcc.Graph(figure=create_heatmap(corr_matrix) if corr_matrix is not None else {})
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

        dbc.Tab(label="📘 Learn More", tab_id="tab-learn", children=[
            html.H4("What Is a Closing Price?"),
            html.P("The closing price is the final price a stock trades at before the market closes for the day."),

            html.H4("What Does 'Normalized to 100' Mean?"),
            html.P("All stocks were adjusted to start at 100 to make comparisons of relative growth easier."),

            html.H4("What Is Correlation?"),
            html.P("Correlation tells us how similarly two stocks move. Close to 1 = move together.")
        ])
    ], id='tabs', active_tab='tab-trends')
