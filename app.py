import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(page_title="Trading Strategy Backtester", layout="wide")


st.title("Algorithmic Trading Strategy Backtester")
st.caption(
    "Simulate how your money could have grown or fallen in the past "
    "by following simple buy & sell rules — no real money involved."
)

st.sidebar.header("Strategy Inputs")

ticker = st.sidebar.text_input("Stock Ticker", value="AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2018-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2025-01-01"))

initial_capital = st.sidebar.number_input(
    "Initial Capital (₹)", value=100000, step=1000
)

sma_short = st.sidebar.slider("Short-Term SMA (days)", 10, 100, 50)
sma_long = st.sidebar.slider("Long-Term SMA (days)", 100, 300, 200)
rsi_period = st.sidebar.slider("RSI Sensitivity (days)", 5, 30, 14)

position_size = st.sidebar.slider("Capital per Trade (%)", 10, 100, 20)
stop_loss_pct = st.sidebar.slider("Stop Loss (%)", 2, 30, 10)
take_profit_pct = st.sidebar.slider("Take Profit (%)", 5, 50, 20)

run_button = st.sidebar.button("Run Strategy")
