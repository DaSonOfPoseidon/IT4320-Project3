# Chart generation
import plotly.graph_objects as go
import webbrowser
import os

def safe_open_browser(path):
    if os.environ.get("CI", "false").lower() != "true":
        webbrowser.open(f"file://{path}")

def generate_chart(data, chart_type, symbol):
    if data.empty:
        print("No data available to generate chart.")
        return None

    # Normalize common Alpha Vantage column names
    cols = {c.lower(): c for c in data.columns}
    open_col = cols.get("1. open") or cols.get("open") or "close"
    high_col = cols.get("2. high") or cols.get("high") or "close"
    low_col = cols.get("3. low") or cols.get("low") or "close"
    close_col = cols.get("4. close") or cols.get("close") or next(iter(cols.values()))
    volume_col = cols.get("5. volume") or cols.get("volume")

    print(f"Generating {chart_type} chart for {symbol}...")

    # Create Plotly figure
    fig = go.Figure()

    # --- LINE CHART ---
    if chart_type == "line":
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data[close_col],
            mode="lines",
            name="Close Price",
            line=dict(color="blue")
        ))

    # --- CANDLESTICK CHART ---
    elif chart_type == "candlestick":
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data[open_col],
            high=data[high_col],
            low=data[low_col],
            close=data[close_col],
            name="Candlestick"
        ))
        fig.update_xaxes(rangeslider_visible=False)

    # --- BAR CHART ---
    elif chart_type == "bar":
        fig.add_trace(go.Bar(
            x=data.index,
            y=data[close_col],
            name="Close Price",
            marker_color="orange"
        ))

    # --- AREA CHART ---
    elif chart_type == "area":
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data[close_col],
            fill="tozeroy",
            mode="lines",
            name="Close Price",
            line=dict(color="green")
        ))

    # --- VOLUME OVERLAY CHART ---
    elif chart_type == "volume":
        # Price as line chart
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data[close_col],
            mode="lines",
            name="Close Price",
            line=dict(color="blue"),
            yaxis="y1"
        ))

        # Volume as bar overlay (secondary axis)
        if volume_col and volume_col in data.columns:
            fig.add_trace(go.Bar(
                x=data.index,
                y=data[volume_col],
                name="Volume",
                marker_color="rgba(255, 165, 0, 0.5)",
                yaxis="y2"
            ))
        else:
            print("Volume data not found — showing price only.")

        fig.update_layout(
            yaxis=dict(title="Price (USD)", side="left"),
            yaxis2=dict(
                title="Volume",
                overlaying="y",
                side="right",
                showgrid=False
            )
        )

    else:
        print(f"Unsupported chart type: {chart_type}")
        return None

    # Layout styling
    fig.update_layout(
        title=f"{symbol.upper()} Stock Data ({chart_type.capitalize()} Chart)",
        xaxis_title="Date",
        template="plotly_dark",
        hovermode="x unified",
        legend=dict(x=0, y=1)
    )

    # Save and open HTML chart
    output_path = os.path.abspath(f"{symbol}_{chart_type}_chart.html")
    fig.write_html(output_path)
    safe_open_browser(output_path)

    print(f"Chart saved to: {output_path}")
    return output_path

