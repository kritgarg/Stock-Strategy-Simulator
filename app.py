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
