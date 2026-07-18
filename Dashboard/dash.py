import streamlit as st
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.loader import load_new, load_raw, save
from plots.plotly_plots import show_candle_stick, show_returns_volatility, show_drawdown, show_anomaly_detection, show_fat_tails, show_correlation_heatmap


st.set_page_config(page_title="SPEDA", layout="wide")

def loading(ticker, period, save_name):
    df = load_new(ticker, period)
    save(df, save_name)
    df_loaded = load_raw(save_name)
    st.text("Saved and loaded successfully")
    st.session_state.loaded_at = pd.Timestamp.now().strftime("%H:%M:%S")
    return df_loaded



@st.dialog("Load Stock Data")
def input_dialog():
    if "step" not in st.session_state:
        st.session_state.step = 1
    if st.session_state.step == 1:
        popular = ["", "META", "AAPL", "GOOGL", "MSFT", "TSLA", "NVDA", "AMZN", "SPY", "QQQ"]
        quick = st.selectbox("Quick Select", popular)
        if quick:
            st.session_state.ticker = quick
        st.session_state.ticker = st.text_input("Or enter ticker", value=st.session_state.get("ticker", ""))
        st.session_state.save_name = st.text_input("File Name")
        if st.button("Next"):
            st.session_state.step = 2
    elif st.session_state.step == 2:
        st.session_state.period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y"])
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Back"):
                st.session_state.step = 1
        with col2:
            if st.button("Load", use_container_width=True):
                with st.spinner("Fetching data..."):
                    st.session_state.df = loading(
                        st.session_state.ticker,
                        st.session_state.period,
                        st.session_state.save_name
                    )
                st.session_state.step = 1
                st.rerun()

@st.dialog("Load Saved Data")
def load_saved_dialog():
    files = os.listdir("csv_saves")
    selected = st.selectbox("Select File", files)
    if st.button("Load"):
        with st.spinner("Loading..."):
            st.session_state.df = load_raw(selected.replace(".csv", ""))
            st.session_state.ticker = selected.replace(".csv", "")
            st.session_state.period = "saved"
            st.session_state.step = 1
        st.session_state.loaded_at = pd.Timestamp.now().strftime("%H:%M:%S")
        st.rerun()


with st.sidebar:
    st.header("Settings")
    rolling_window = st.slider("Rolling Window", min_value=5, max_value=60, value=20, step=1)

#title+info
st.title("SPEDA — Stock Price Exploratory Data Analysis")
if "df" in st.session_state:
    st.caption(f"{st.session_state.ticker} · {st.session_state.period} · {len(st.session_state.df)} rows · loaded {st.session_state.get('loaded_at', '')}")

#triggers
if "df" not in st.session_state:
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Load Stock Data"):
            input_dialog()
    with col2:
        if st.button("Load Saved"):
            load_saved_dialog()
else:
    st.success(f"Loaded: {st.session_state.get('ticker')} | {st.session_state.get('period')}")
    if st.button("Load New Data"):
        del st.session_state["df"]
        st.rerun()


tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview",
    "Price Overview",
    "Returns & Volatility",
    "Drawdown",
    "Anomaly Detection",
    "Fat Tails",
    "Correlation Matrix"
])
with tab0:
    if "df" in st.session_state:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(show_candle_stick(st.session_state.df), use_container_width=True, config={"scrollZoom": True}, key="ov_candle")
            st.plotly_chart(show_drawdown(st.session_state.df, rolling=rolling_window), use_container_width=True, config={"scrollZoom": True}, key="ov_drawdown")
            st.plotly_chart(show_fat_tails(st.session_state.df), use_container_width=True, config={"scrollZoom": True}, key="ov_fattails")
        with col2:
            st.plotly_chart(show_returns_volatility(st.session_state.df, rolling=rolling_window), use_container_width=True, config={"scrollZoom": True}, key="ov_returns")
            if len(st.session_state.df) >= 40:
                charts = show_anomaly_detection(st.session_state.df, rolling=rolling_window)
                st.plotly_chart(charts["Combined (All Methods)"](), use_container_width=True, config={"scrollZoom": True}, key="ov_anomaly")
            st.plotly_chart(show_correlation_heatmap(st.session_state.df, ["Open", "High", "Low", "Close", "Volume"], window=rolling_window), use_container_width=True, config={"scrollZoom": True}, key="ov_corr")
    else:
        st.info("Load a stock to get started.")
with tab1:
    if "df" in st.session_state:
        fig = show_candle_stick(st.session_state.df)
        st.plotly_chart(fig, use_container_width=True, config={
            "scrollZoom": True,
            "modeBarButtonsToRemove": ["select2d", "lasso2d", "zoom2d"],
            "modeBarButtonsToAdd": ["pan2d"],
        })
    else:
        st.info("Load a stock to get started.")

with tab2:
    if "df" in st.session_state:
        fig = show_returns_volatility(st.session_state.df, rolling=rolling_window)
        st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True})
        st.caption("Tip: load at least 1 year of data for meaningful volatility patterns. Short periods will appear flat.")
    else:
        st.info("Load a stock to get started.")

with tab3:
    if "df" in st.session_state:
        fig = show_drawdown(st.session_state.df, rolling=rolling_window)
        st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True})
    else:    
        st.info("Load a stock to get started")

with tab4:
    if "df" in st.session_state:
        if len(st.session_state.df) < 40:
            st.warning("Not enough data for anomaly detection — load at least 3 months.")
        else:
            charts = show_anomaly_detection(st.session_state.df, rolling=rolling_window)
            method = st.selectbox("Method", list(charts.keys()))
            st.plotly_chart(charts[method](), use_container_width=True, config={"scrollZoom": True})
    else:
        st.info("Load a stock to get started.")

with tab5:
    if "df" in st.session_state:
        fig = show_fat_tails(st.session_state.df)
        st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True})
        st.caption("Kurtosis > 3 indicates fat tails (more extreme returns than a normal distribution). Skewness < 0 indicates left-skewed returns (more frequent large losses than gains).")
    else:
        st.info("Load a stock to get started.")

with tab6:
    if "df" in st.session_state:
        presets = {
            "Price Action": ["Open", "High", "Low", "Close", "Volume"],
            "Returns Based": ["Return", "Volatility", "Drawdown"],
            "Full": ["Open", "High", "Low", "Close", "Volume", "Return", "Volatility", "Drawdown"],
        }
        col1, col2 = st.columns([3, 1])
        with col1:
            preset = st.selectbox("Preset", list(presets.keys()))
        with col2:
            rolling = st.toggle("Rolling", value=False)
        fig = show_correlation_heatmap(st.session_state.df, presets[preset], rolling=rolling, window=rolling_window)
        st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True})
    else:
        st.info("Load a stock to get started.")
