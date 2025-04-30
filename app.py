from dash import Dash, Output, Input, html
import dash_bootstrap_components as dbc
import pandas as pd
from callbacks import register_callbacks
from tabs import get_tabs
from data.data_downloader import prepare_time_series, prepare_correlation_matrix
from visuals.time_series import create_time_series_chart

# --- Load Data ---
time_series_df = prepare_time_series()
corr_matrix = prepare_correlation_matrix()

# --- Initialize App ---
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.MINTY])
app.title = "NVIDIA Market Influence Dashboard"

register_callbacks(app, time_series_df)

app.layout = html.Div([
    html.H1("NVIDIA: The Stock That Moves the Market", style={"textAlign": "center", "marginTop": "20px"}),
    get_tabs(time_series_df, corr_matrix)
])


if __name__ == "__main__":
    app.run_server(debug=True)
