# Streamlit Stock Chart Generator
# Ultra-simple alternative to Flask + Plotly

import streamlit as st
import plotly.graph_objects as go
from src.api_client import AlphaVantageClient
from src.data_processor import filter_date_range

# Page config
st.set_page_config(page_title="Stock Chart Generator", page_icon="📈", layout="wide")

# Title
st.title("📈 Stock Chart Generator")
st.markdown("Visualize stock market data with interactive charts")

# Sidebar for inputs
st.sidebar.header("Chart Configuration")

# Stock symbol input
symbol = st.sidebar.selectbox(
    "Stock Symbol",
    ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NVDA", "JPM", "V", "JNJ"]
)

# Chart type
chart_type = st.sidebar.selectbox(
    "Chart Type",
    ["Line", "Candlestick", "OHLC", "Volume Overlay"]
)

# Time series
time_series = st.sidebar.selectbox(
    "Time Series",
    ["Daily", "Weekly", "Monthly"]
)

# Date range (optional)
st.sidebar.subheader("Date Range (Optional)")
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=None)
with col2:
    end_date = st.date_input("End Date", value=None)

# Generate button
if st.sidebar.button("Generate Chart 🚀", type="primary"):
    try:
        # Show loading spinner
        with st.spinner("Fetching data and generating chart..."):
            # Map selections to API parameters
            time_series_map = {
                "Daily": "TIME_SERIES_DAILY",
                "Weekly": "TIME_SERIES_WEEKLY",
                "Monthly": "TIME_SERIES_MONTHLY"
            }

            # Fetch data
            client = AlphaVantageClient()
            data = client.fetch_stock_data(symbol, time_series_map[time_series])

            # Filter by date range if provided
            if start_date and end_date:
                data = filter_date_range(data, str(start_date), str(end_date))

            # Get columns
            cols = {c.lower(): c for c in data.columns}
            open_col = cols.get("open", "Close")
            high_col = cols.get("high", "Close")
            low_col = cols.get("low", "Close")
            close_col = cols.get("close")
            volume_col = cols.get("volume")

            # Create figure
            fig = go.Figure()

            if chart_type == "Line":
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data[close_col],
                    mode="lines",
                    name="Close Price",
                    line=dict(color="blue")
                ))

            elif chart_type == "Candlestick":
                fig.add_trace(go.Candlestick(
                    x=data.index,
                    open=data[open_col],
                    high=data[high_col],
                    low=data[low_col],
                    close=data[close_col],
                    name="Candlestick"
                ))

            elif chart_type == "OHLC":
                fig.add_trace(go.Ohlc(
                    x=data.index,
                    open=data[open_col],
                    high=data[high_col],
                    low=data[low_col],
                    close=data[close_col],
                    name="OHLC"
                ))

            elif chart_type == "Volume Overlay":
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data[close_col],
                    mode="lines",
                    name="Close Price",
                    line=dict(color="blue"),
                    yaxis="y1"
                ))

                if volume_col:
                    fig.add_trace(go.Bar(
                        x=data.index,
                        y=data[volume_col],
                        name="Volume",
                        marker_color="rgba(255, 165, 0, 0.5)",
                        yaxis="y2"
                    ))

                fig.update_layout(
                    yaxis=dict(title="Price (USD)", side="left"),
                    yaxis2=dict(title="Volume", overlaying="y", side="right", showgrid=False)
                )

            # Update layout
            fig.update_layout(
                title=f"{symbol} Stock Data ({chart_type} Chart)",
                xaxis_title="Date",
                template="plotly_dark",
                hovermode="x unified",
                height=600
            )

            # Display the chart - THIS IS ALL IT TAKES!
            st.plotly_chart(fig, use_container_width=True)

            # Show data info
            st.success(f"✅ Chart generated successfully!")
            st.info(f"📊 Showing {len(data)} data points from {data.index.min()} to {data.index.max()}")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.exception(e)

else:
    # Show instructions
    st.info("👈 Configure your chart settings in the sidebar and click 'Generate Chart' to get started!")

    # Show example
    st.markdown("""
    ### Features:
    - 📈 Multiple chart types (Line, Candlestick, OHLC, Volume)
    - 📅 Flexible time series (Daily, Weekly, Monthly)
    - 🎯 Date range filtering
    - 🔄 Interactive Plotly charts
    - ⚡ Fast and responsive

    ### Instructions:
    1. Select a stock symbol from the sidebar
    2. Choose your preferred chart type
    3. Select the time series granularity
    4. Optionally set a date range
    5. Click "Generate Chart"
    """)
