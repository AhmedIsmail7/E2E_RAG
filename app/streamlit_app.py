import streamlit as st
import numpy as np
import pandas as pd
import time

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & GLOBAL STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Advanced Portfolio Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. OPTIMIZED DATA CACHING
# -----------------------------------------------------------------------------
@st.cache_data(ttl=600)  # Caches result for 10 minutes to save system resources
def fetch_historical_data(ticker):
    """Simulates a heavy, slow API call to fetch stock history data."""
    time.sleep(1.5)  # Simulate latency
    dates = pd.date_range(start="2026-01-01", periods=100)
    prices = 100 + np.random.randn(100).cumsum() * (3 if ticker == "AAPL" else 5)
    return pd.DataFrame({"Date": dates, "Price": prices}).set_index("Date")

# -----------------------------------------------------------------------------
# 3. GLOBAL STATE & NAVIGATION
# -----------------------------------------------------------------------------
if "portfolio_value" not in st.session_state:
    st.session_state.portfolio_value = 50_000.00

with st.sidebar:
    st.header("⚡ Global Controls")
    selected_ticker = st.selectbox("Select Asset Class:", ["AAPL", "TSLA", "NVDA"])
    
    # Session State Mutation
    deposit = st.number_input("Deposit Funds ($):", min_value=0, value=0, step=1000)
    if st.button("Update Portfolio Balance", use_container_width=True):
        st.session_state.portfolio_value += deposit
        st.toast(f"Successfully deposited ${deposit:,.2f}!", icon="💰")

# -----------------------------------------------------------------------------
# 4. MAIN DASHBOARD CONTENT
# -----------------------------------------------------------------------------
st.title("📈 Advanced Real-Time Analytics Dashboard")
st.caption("Demonstrating Fragmented Rendering, Smart Caching, and Session Management")

# High-Performance Data Loading Banner
with st.spinner(f"Querying analytical engines for {selected_ticker}..."):
    stock_df = fetch_historical_data(selected_ticker)

# Layout Grid: Metrics Cards
col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.metric(label="Total Portfolio Balance", value=f"${st.session_state.portfolio_value:,.2f}")
with col2:
    with st.container(border=True):
        latest_price = stock_df["Price"].iloc[-1]
        pct_change = ((latest_price - stock_df["Price"].iloc[0]) / stock_df["Price"].iloc[0]) * 100
        st.metric(label=f"Latest {selected_ticker} Value", value=f"${latest_price:.2f}", delta=f"{pct_change:.2f}%")
with col3:
    with st.container(border=True):
        st.metric(label="System Engine Status", value="Operational", delta="Optimal Latency", delta_color="normal")

# -----------------------------------------------------------------------------
# 5. HIGH-ADVANCED FEATURE: ISOLATED RENDERING VIA FRAGMENTS
# -----------------------------------------------------------------------------
@st.fragment(run_every="5s")
def live_order_book():
    """Reruns independently every 5 seconds without triggering global page refreshes."""
    st.subheader("🔄 Isolated Live Order Book Feed (Auto-Refreshes)")
    
    # Generate dynamic volatile data
    live_bids = pd.DataFrame({
        "Price ($)": np.round(latest_price + np.random.uniform(-1.5, 1.5, 5), 2),
        "Volume (Shares)": np.random.randint(100, 2500, 5)
    }).sort_values(by="Price ($)", ascending=False)
    
    col_table, col_widget = st.columns([2, 1])
    
    with col_table:
        # Highlighting row interactivity
        st.dataframe(live_bids, use_container_width=True, hide_index=True)
    
    with col_widget:
        st.info("Notice that moving the noise toggle below scales local data without forcing a global page reload.")
        noise_level = st.slider("Local Blur Noise Filter:", 1, 10, 3)
        st.caption(f"Noise filter active setting: {noise_level}x")

# Main Chart Display
st.line_chart(stock_df, y="Price", use_container_width=True)

# Run the isolated component block
live_order_book()
