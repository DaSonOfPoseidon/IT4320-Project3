# /usr/bin/env python3
# Flask Web Application for Stock Chart Generator
# Provides web interface for Alpha Vantage stock data visualization

import json
from flask import Flask, render_template, request
import plotly.graph_objects as go
import plotly.io as pio

from src.api_client import (
    AlphaVantageClient,
    APIError,
    RateLimitError,
    InvalidSymbolError,
    NetworkError,
)
from src.data_processor import filter_date_range
from src.constants import CHART_TYPES, TIME_SERIES_FUNCTIONS

app = Flask(__name__)


# Load stock symbols from JSON file
def load_stock_symbols():
    """Load stock symbols from stock_symbols.json file."""
    try:
        with open("stock_symbols.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Return a default list if file not found
        return [
            {"symbol": "AAPL", "name": "Apple Inc."},
            {"symbol": "GOOGL", "name": "Alphabet Inc."},
            {"symbol": "MSFT", "name": "Microsoft Corporation"},
        ]


def generate_web_chart(data, chart_type, symbol):
    """
    Generate chart for web display (returns Plotly JSON instead of saving HTML file).

    Args:
        data: pandas DataFrame with stock data
        chart_type: Type of chart to generate ('line', 'candlestick', 'ohlc', 'volume')
        symbol: Stock symbol

    Returns:
        Plotly figure JSON and chart info dictionary
    """
    if data.empty:
        raise ValueError("No data available to generate chart.")

    # Normalize column names (handle Alpha Vantage API response format)
    # Create a case-insensitive lookup dictionary
    cols = {c.lower(): c for c in data.columns}

    # Helper function to find column name with multiple fallbacks
    def find_column(patterns, fallback=None):
        """Find column name using multiple pattern matches."""
        for pattern in patterns:
            if pattern.lower() in cols:
                return cols[pattern.lower()]
        return fallback

    # Find columns with proper fallback logic
    # Try: original API format, cleaned lowercase, capitalized
    open_col = find_column(["1. open", "open", "Open"], "Close")
    high_col = find_column(["2. high", "high", "High"], "Close")
    low_col = find_column(["3. low", "low", "Low"], "Close")
    close_col = find_column(["4. close", "close", "Close"], None)
    volume_col = find_column(["5. volume", "volume", "Volume"], None)

    # Validate that we found the close column at minimum
    if not close_col or close_col not in data.columns:
        raise ValueError(
            f"Could not find close price column in data. Available columns: {data.columns.tolist()}"
        )

    # Convert to plain Python lists for better JSON serialization
    data = data.copy()
    date_list = data.index.to_pydatetime().tolist()

    # Convert all data columns to lists to avoid pandas serialization issues
    close_list = data[close_col].tolist()
    open_list = data[open_col].tolist() if open_col in data.columns else close_list
    high_list = data[high_col].tolist() if high_col in data.columns else close_list
    low_list = data[low_col].tolist() if low_col in data.columns else close_list
    volume_list = data[volume_col].tolist() if volume_col and volume_col in data.columns else None

    fig = go.Figure()

    # --- LINE CHART ---
    if chart_type == "line":
        fig.add_trace(
            go.Scatter(
                x=date_list, y=close_list, mode="lines", name="Close Price", line=dict(color="#FFC107", width=2)
            )
        )

    # --- CANDLESTICK CHART ---
    elif chart_type == "candlestick":
        fig.add_trace(
            go.Candlestick(
                x=date_list,
                open=open_list,
                high=high_list,
                low=low_list,
                close=close_list,
                name="Candlestick",
                increasing_line_color="#FFC107",
                decreasing_line_color="#000000",
                increasing_fillcolor="#FFD54F",
                decreasing_fillcolor="#424242",
            )
        )
        fig.update_xaxes(rangeslider_visible=False)

    # --- OHLC CHART ---
    elif chart_type == "ohlc":
        fig.add_trace(
            go.Ohlc(
                x=date_list,
                open=open_list,
                high=high_list,
                low=low_list,
                close=close_list,
                name="OHLC",
                increasing_line_color="#FFC107",
                decreasing_line_color="#000000",
            )
        )
        fig.update_xaxes(rangeslider_visible=False)

    # --- VOLUME OVERLAY CHART ---
    elif chart_type == "volume":
        fig.add_trace(
            go.Scatter(
                x=date_list,
                y=close_list,
                mode="lines",
                name="Close Price",
                line=dict(color="#FFC107", width=2),
                yaxis="y1",
            )
        )

        if volume_list:
            fig.add_trace(
                go.Bar(
                    x=date_list,
                    y=volume_list,
                    name="Volume",
                    marker_color="rgba(255, 193, 7, 0.3)",
                    yaxis="y2",
                )
            )

        fig.update_layout(
            yaxis=dict(title="Price (USD)", side="left"),
            yaxis2=dict(title="Volume", overlaying="y", side="right", showgrid=False),
        )

    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")

    # Layout styling
    fig.update_layout(
        title=f"{symbol.upper()} Stock Data ({chart_type.capitalize()} Chart)",
        title_font=dict(size=24, color="#FFC107"),
        xaxis_title="Date",
        template="plotly_dark",
        hovermode="x unified",
        legend=dict(x=0, y=1, bgcolor="rgba(0,0,0,0.7)", bordercolor="#FFC107", borderwidth=1),
        plot_bgcolor="#1a1a1a",
        paper_bgcolor="#0d0d0d",
        font=dict(color="#FFD54F"),
        xaxis=dict(gridcolor="#333333", color="#FFC107"),
        yaxis=dict(gridcolor="#333333", color="#FFC107"),
    )

    # Convert figure to JSON string
    # Plotly handles datetime and numpy types properly with to_json
    chart_json_str = pio.to_json(fig, engine="json")

    # Parse it back to dict so Jinja can serialize it
    chart_dict = json.loads(chart_json_str)

    return chart_dict


@app.route("/")
def index():
    """Render the main form page."""
    stocks = load_stock_symbols()
    return render_template("index.html", stocks=stocks)


@app.route("/generate-chart", methods=["POST"])
def generate_chart():
    """
    Handle chart generation request from web form.
    Fetches data from API, processes it, and returns chart page.
    """
    try:
        # Get form data
        symbol = request.form.get("symbol", "").upper().strip()
        chart_type_id = request.form.get("chart_type", "")
        time_series_id = request.form.get("time_series", "")
        interval = request.form.get("interval", "")
        start_date_str = request.form.get("start_date", "")
        end_date_str = request.form.get("end_date", "")

        # Validate required fields
        if not symbol:
            raise ValueError("Stock symbol is required")
        if not chart_type_id:
            raise ValueError("Chart type is required")
        if not time_series_id:
            raise ValueError("Time series function is required")

        # Get chart type and time series details from constants
        chart_type_info = CHART_TYPES.get(chart_type_id)
        time_series_info = TIME_SERIES_FUNCTIONS.get(time_series_id)

        if not chart_type_info:
            raise ValueError(f"Invalid chart type: {chart_type_id}")
        if not time_series_info:
            raise ValueError(f"Invalid time series function: {time_series_id}")

        chart_type_key = chart_type_info["key"]
        time_series_function = time_series_info["key"]

        # Validate interval for intraday
        if time_series_info.get("requires_interval") and not interval:
            raise ValueError("Interval is required for intraday time series")

        # Initialize API client
        api_client = AlphaVantageClient()

        # Fetch stock data
        if time_series_function == "TIME_SERIES_INTRADAY":
            data = api_client.fetch_stock_data(symbol, time_series_function, interval=interval)
        else:
            data = api_client.fetch_stock_data(symbol, time_series_function)

        # Filter data by date range if provided
        if start_date_str and end_date_str:
            data = filter_date_range(data, start_date_str, end_date_str)
        else:
            # If no date range specified, limit to last 500 data points for performance
            # (Full historical data can cause browser performance issues)
            if len(data) > 500:
                data = data.tail(500)

        # Generate chart
        chart_dict = generate_web_chart(data, chart_type_key, symbol)

        # Prepare chart information for display
        chart_info = {
            "symbol": symbol,
            "chart_type": chart_type_info["display"],
            "time_series": time_series_info["display"],
            "date_range": None,
        }

        if start_date_str and end_date_str:
            chart_info["date_range"] = f"{start_date_str} to {end_date_str}"
        elif start_date_str:
            chart_info["date_range"] = f"From {start_date_str}"
        elif end_date_str:
            chart_info["date_range"] = f"Until {end_date_str}"

        # Render result page with chart
        return render_template(
            "result.html",
            title=f"{symbol} {chart_type_info['display']}",
            subtitle=f"{time_series_info['display']} visualization",
            chart_dict=chart_dict,
            chart_info=chart_info,
        )

    except (APIError, RateLimitError, InvalidSymbolError, NetworkError) as e:
        # Handle API-specific errors
        return render_template("error.html", error_message=str(e), error_type=type(e).__name__), 400

    except ValueError as e:
        # Handle validation errors
        return (
            render_template("error.html", error_message=str(e), error_type="ValidationError"),
            400,
        )

    except Exception as e:
        # Handle unexpected errors
        return (
            render_template(
                "error.html",
                error_message=f"An unexpected error occurred: {str(e)}",
                error_type="UnexpectedError",
            ),
            500,
        )


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return (
        render_template(
            "error.html",
            error_message="Page not found. The URL you requested does not exist.",
            error_type="404 Not Found",
        ),
        404,
    )


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return (
        render_template(
            "error.html",
            error_message="Internal server error. Please try again later.",
            error_type="500 Internal Server Error",
        ),
        500,
    )


if __name__ == "__main__":
    # Run Flask development server
    # For production, use a WSGI server like Gunicorn
    app.run(host="0.0.0.0", port=5000, debug=True)
