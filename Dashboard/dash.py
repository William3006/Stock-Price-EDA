import streamlit as st
import pandas as pd
import sys
sys.path.append("..")
from data.loader import load_new, load_raw, save


# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="SPEDA", layout="wide")
st.title("SPEDA — Stock Price Exploratory Data Analysis")

# ── sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Controls")
    ticker = st.text_input("Ticker", value="META")
    period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y"], index=3)

# ── data loading ──────────────────────────────────────────────────────────────


def loading(ticker, period, save_name):
    df = load_new(ticker, period)
    save(df, save_name)
    df_loaded = load_raw(save_name)
    st.text("Saved and loaded successfully")
    return df_loaded

@st.dialog("Load Stock Data")
def input_dialog():
    if "step" not in st.session_state:
        st.session_state.step = 1

    if st.session_state.step == 1:
        st.session_state.ticker = st.text_input("Ticker")
        st.session_state.save_name = st.text_input("File Name")
        if st.button("Next"):
            st.session_state.step = 2
            st.rerun()

    elif st.session_state.step == 2:
        st.session_state.period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y"])
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Back"):
                st.session_state.step = 1
                st.rerun()
        with col2:
            if st.button("Load", use_container_width=True):
                with st.spinner("Fetching data..."):
                    loading(...)
    
        

# ── tabs ──────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Price Overview",
    "Returns & Volatility",
    "Drawdown",
    "Anomaly Detection",
    "Fat Tails",
    "Correlation Matrix"
])

with tab1:
    st.write("candlestick goes here")

with tab2:
    st.write("returns + rolling vol goes here")

with tab3:
    st.write("drawdown goes here")

with tab4:
    st.write("anomaly detection goes here")

with tab5:
    st.write("fat tails goes here")

with tab6:
    st.write("correlation matrix goes here")

if "data_loaded" not in st.session_state:
    input_dialog()