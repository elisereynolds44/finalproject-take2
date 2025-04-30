import plotly.graph_objects as go

def create_heatmap(corr_matrix):
    label_map = {
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

    if corr_matrix is None or corr_matrix.empty:
        return go.Figure(
            layout={
                "title": "⚠️ Correlation matrix not available.",
                "xaxis": {"visible": False},
                "yaxis": {"visible": False}
            }
        )

    try:
        tickers = corr_matrix.columns.tolist()
        readable_labels = [label_map.get(t, t) for t in tickers]

        fig = go.Figure(
            data=go.Heatmap(
                z=corr_matrix.values,
                x=readable_labels,
                y=readable_labels,
                colorscale='Viridis',
            )
        )
        fig.update_layout(
            title='Stock Price Correlation Heatmap (2023 - 2024)',
            xaxis_title="Company",
            yaxis_title="Company"
        )
        return fig

    except Exception as e:
        print(f"❌ Error creating heatmap: {e}")
        return go.Figure(
            layout={
                "title": "⚠️ Error generating heatmap.",
                "xaxis": {"visible": False},
                "yaxis": {"visible": False}
            }
        )
