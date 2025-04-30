from dash import Dash, Output, Input, html
import dash_bootstrap_components as dbc

from tabs import get_tabs
from data.data_downloader import prepare_time_series, get_stock_data, prepare_correlation_matrix
from visuals.time_series import create_time_series_chart

# --- Get and prepare data ---
stock_data = get_stock_data()
time_series_df = prepare_time_series(stock_data)
corr_matrix = prepare_correlation_matrix(stock_data)

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.MINTY])
app.title = "NVIDIA Market Influence Dashboard"

app.layout = html.Div([
    html.H1("NVIDIA: The Stock That Moves the Market", style={"textAlign": "center", "marginTop": "20px"}),
    get_tabs(time_series_df, corr_matrix)
])

# --- Callback for time series chart ---
@app.callback(
    Output("time-series-chart", "figure"),
    Input("stock-selector", "value")
)
def update_chart(selected_stocks):
    if time_series_df is None:
        # Return an empty figure or placeholder if data failed
        return {
            "data": [],
            "layout": {
                "title": "⚠️ Data unavailable. Please try again later.",
                "xaxis": {"visible": False},
                "yaxis": {"visible": False}
            }
        }
    return create_time_series_chart(time_series_df, selected_stocks)

# --- Run App ---
if __name__ == "__main__":
    app.run_server(debug=True)
