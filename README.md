# Algorithmic Trading Strategy Backtester

A professional-grade, web-based simulation tool that allows users to backtest algorithmic trading strategies using historical market data. Built with Python and Streamlit, this application bridges the gap between complex financial concepts and accessible user experimentation without financial risk.

## 📌 About the Project

This project was developed to demonstrate how algorithmic trading strategies can be visualized and tested against historical data. It focuses on the **Golden Cross** strategy combined with **RSI (Relative Strength Index)** indicators and robust risk management controls (Stop Loss and Take Profit).

The simulator allows users—even those with no prior trading experience—to understand how technical indicators interact to generate buy and sell signals.

## 🚀 Problem & Solution

**The Problem:**
Algorithmic trading often feels like a "black box" to beginners. Understanding how moving averages, momentum indicators, and risk management settings affect long-term profitability is difficult without writing complex code or risking real capital.

**The Solution:**
A beautifully designed, interactive web application that:
1.  **Democratizes Access:** Provides an easy-to-use interface for complex calculations.
2.  **Visualizes Logic:** Shows exactly where buy and sell signals occur on the price chart.
3.  **Enforces Risk Management:** Simulates real-world constraints like Position Sizing, Stop Losses, and Take Profits.

## ✨ Key Features

-   **Dynamic Strategy Customization:** Adjust Short/Long SMA windows and RSI thresholds in real-time.
-   **Risk Management Simulation:** Configure Position Sizing, Stop Loss %, and Take Profit % to test risk-adjusted returns.
-   **Interactive Visualization:** Plot buy/sell signals directly on price charts using Matplotlib.
-   **Detailed Performance Metrics:** Instant calculation of Strategy Return vs. Buy & Hold Return.
-   **Trade Log Transparency:** Full table view of every simulated trade execution.

## 🛠️ Tech Stack

-   **Frontend:** Streamlit (Python-based reactive UI)
-   **Data Source:** `yfinance` (Yahoo Finance API)
-   **Data Processing:** Pandas (Time-series analysis)
-   **Visualization:** Matplotlib
-   **Language:** Python 3.9+

## 📸 Screenshots

| Strategy Inputs | Result Visualization |
|:---:|:---:|
| ![Strategy Inputs](docs/images/inputs_placeholder.png) | ![Results Chart](docs/images/chart_placeholder.png) |

*(Note: Replace `docs/images/` paths with actual screenshots after deployment)*

## ⚙️ Environment Variables

No sensitive environment variables are required for this project as it uses the public Yahoo Finance API.

## 📦 Installation

To run this project locally, follow these steps:

1.  **Clone the repository**
    ```bash
    git clone https://github.com/kritgarg/Stock-Strategy-Simulator.git
    cd Stock-Strategy-Simulator
    ```

2.  **Create a virtual environment (optional but recommended)**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**
    ```bash
    streamlit run app.py
    ```

## 📂 Folder Structure

```
Stock-Strategy-Simulator/
├── app.py                # Main application entry point
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
└── docs/                 # Documentation assets (images, guides)
```

## 📜 Documentation & Policy

### Disclaimer
**This application is for educational purposes only.** The results generated are simulations based on historical data and do not guarantee future performance. This tool does not provide financial advice.

### Logic Overview
-   **SMA (Simple Moving Average):** Calculates the average price over a specific window to smooth out price data.
-   **RSI (Relative Strength Index):** Measures the speed and change of price movements.
-   **Signal Generation:**
    -   **Buy:** Short-term trend crosses above Long-term trend AND RSI indicates asset is not overbought.
    -   **Sell:** Short-term trend crosses below Long-term trend OR RSI indicates asset is overbought.

## 🗺️ Roadmap

-   [ ] Add support for multiple stock tickers comparison.
-   [ ] Implement Exponential Moving Averages (EMA).
-   [ ] Add "Sharpe Ratio" and "Max Drawdown" to metrics.
-   [ ] Export trade logs to CSV.

## 👨‍💻 Author

**Krit Garg**
-   [GitHub](https://github.com/kritgarg)
-   [LinkedIn](https://linkedin.com/in/kritgarg)

---

*Built with ❤️ using Streamlit and Python.*
