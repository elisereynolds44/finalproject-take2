import plotly.graph_objects as go

def create_heatmap(corr_matrix):
    # If your CSV column names are already full company names (they are), you can use them directly
    if corr_matrix is None or corr_matrix.empty:
        return go.Figure(
            layout={
                "title": "⚠️ Correlation matrix not available.",
                "xaxis": {"visible": False},
                "yaxis": {"visible": False}
            }
        )

    try:
        # Use the column names directly (since you've labeled them like "NVIDIA", "AMD", etc.)
        labels = corr_matrix.columns.tolist()

        fig = go.Figure(
            data=go.Heatmap(
                z=corr_matrix.values,
                x=labels,
                y=labels,
                colorscale='Viridis',
                zmin=0,  # ensures consistent scale
                zmax=1
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
