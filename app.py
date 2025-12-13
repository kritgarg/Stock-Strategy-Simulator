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



if not run_button:
    st.markdown("## What do these inputs actually mean?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Short-Term SMA (Simple Moving Average)")
        st.caption(
            "This is the **average stock price of the last few days**.\n\n"
            "• Smaller value (like 20 days) reacts quickly to price changes\n"
            "• Used to detect **recent trend direction**"
        )

        st.markdown("###  Long-Term SMA (Simple Moving Average)")
        st.caption(
            "This is the **average stock price over many days**.\n\n"
            "• Larger value (like 200 days) changes slowly\n"
            "• Used to understand the **overall market direction**"
        )

        st.markdown("### How SMA works in this app")
        st.caption(
            "• When **Short SMA goes above Long SMA → trend is upward (BUY allowed)**\n"
            "• When **Short SMA goes below Long SMA → trend weakens (SELL)**"
        )

    with col2:
        st.markdown("### RSI (Relative Strength Index)")
        st.caption(
            "RSI measures **how fast the price is moving**.\n\n"
            "• RSI < 40 → price is relatively low → safer to buy\n"
            "• RSI > 70 → price is very high → risky to buy"
        )

        st.markdown("### Capital per Trade (%)")
        st.caption(
            "Controls **how much of your money is used in one trade**.\n\n"
            "• 20% = safer (money spread over time)\n"
            "• 100% = very risky (all money at once)"
        )

        st.markdown("### Stop Loss (%)")
        st.caption(
            "Limits how much you can lose in a single trade.\n\n"
            "• Example: 10% stop loss → trade exits if price falls 10%\n"
            "• Protects your capital from big crashes"
        )

        st.markdown("### Take Profit (%)")
        st.caption(
            "Locks profit automatically.\n\n"
            "• Example: 20% take profit → sell after 20% gain\n"
            "• Prevents giving back profits"
        )

    st.success(
        "👉 After you click **Run Strategy**, this explanation disappears and "
        "you will only see results, charts, and trade history."
    )


def calculate_rsi(close, period):
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# ----------main logic -------------
if run_button:
    st.subheader(f"📊 Results for {ticker}")

    data = yf.download(ticker, start=start_date, end=end_date)

    if data.empty:
        st.error("❌ Invalid ticker or no data.")
        st.stop()

    # INDICATORS
    data['SMA_SHORT'] = data['Close'].rolling(sma_short).mean()
    data['SMA_LONG'] = data['Close'].rolling(sma_long).mean()
    data['RSI'] = calculate_rsi(data['Close'], rsi_period)

    # SIGNALS
    data['Signal'] = 0
    data.loc[
        (data['SMA_SHORT'] > data['SMA_LONG']) & (data['RSI'] < 40),
        'Signal'
    ] = 1
    data.loc[
        (data['SMA_SHORT'] < data['SMA_LONG']) | (data['RSI'] > 70),
        'Signal'
    ] = -1

    data = data.dropna().copy()

    # BACKTESTING
    capital = float(initial_capital)
    shares = 0
    buy_price = 0
    trade_log = []

    for i in range(len(data)):
        price = float(data['Close'].iloc[i])
        signal = int(data['Signal'].iloc[i])
        date = data.index[i]

        if signal == 1 and shares == 0:
            trade_capital = capital * (position_size / 100)
            shares = trade_capital // price
            if shares > 0:
                capital -= shares * price
                buy_price = price
                trade_log.append({
                    "Type": "BUY",
                    "Date": date,
                    "Price": price,
                    "Shares": shares
                })

        if shares > 0 and price <= buy_price * (1 - stop_loss_pct / 100):
            capital += shares * price
            trade_log.append({
                "Type": "STOP LOSS",
                "Date": date,
                "Price": price,
                "Shares": shares
            })
            shares = 0

        elif shares > 0 and price >= buy_price * (1 + take_profit_pct / 100):
            capital += shares * price
            trade_log.append({
                "Type": "TAKE PROFIT",
                "Date": date,
                "Price": price,
                "Shares": shares
            })
            shares = 0

        elif signal == -1 and shares > 0:
            capital += shares * price
            trade_log.append({
                "Type": "SELL",
                "Date": date,
                "Price": price,
                "Shares": shares
            })
            shares = 0

    # FINAL VALUES
    first_price = float(data['Close'].iloc[0])
    last_price = float(data['Close'].iloc[-1])

    final_value = capital + shares * last_price
    # OVERALL PROFIT / LOSS LABEL
    # PROFIT / LOSS AMOUNT
    profit_loss_amount = final_value - initial_capital

    if profit_loss_amount > 0:
        pl_text = f" You made a profit of ₹{profit_loss_amount:,.0f}"
        pl_color = "#2ecc71"
    else:
            pl_text = f"You lost ₹{abs(profit_loss_amount):,.0f}"
            pl_color = "#e74c3c"


    buy_hold_shares = initial_capital // first_price
    buy_hold_final = buy_hold_shares * last_price

    strategy_return = ((final_value - initial_capital) / initial_capital) * 100
    buy_hold_return = ((buy_hold_final - initial_capital) / initial_capital) * 100

    st.markdown(
        f"""
        <br>
        <div style="
            padding: 14px;
            border-radius: 10px;
            text-align: center;
            font-size: 22px;
            font-weight: 600;
            color: white;
            background-color: {pl_color};
            margin-bottom: 15px;
        ">
            {pl_text}
        </div>
        <br>
        <br>
        """,
        unsafe_allow_html=True
    )

    # METRICS
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Final Capital", f"₹{final_value:,.0f}")
    col2.metric("📈 Strategy Return", f"{strategy_return:.2f}%")
    col3.metric("📊 Buy & Hold Return", f"{buy_hold_return:.2f}%")

    # CHART
    st.subheader("📉 Price Chart with Signals")
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(data.index, data['Close'], label="Price")
    ax.plot(data.index, data['SMA_SHORT'], "--", label="Short Trend")
    ax.plot(data.index, data['SMA_LONG'], "--", label="Long Trend")

    buys = [t for t in trade_log if t["Type"] == "BUY"]
    exits = [t for t in trade_log if t["Type"] != "BUY"]

    ax.scatter([t["Date"] for t in buys], [t["Price"] for t in buys], marker="^", s=120, label="BUY")
    ax.scatter([t["Date"] for t in exits], [t["Price"] for t in exits], marker="v", s=120, label="EXIT")

    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # TRADE LOG
    st.subheader("📋 Trade Log")
    st.dataframe(pd.DataFrame(trade_log))
