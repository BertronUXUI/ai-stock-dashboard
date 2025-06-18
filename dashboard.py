import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

st.set_page_config(page_title="AI Stock Dashboard Demo", layout="wide")
st.title("📊 Stock Summary")

# Input ticker symbol
ticker = st.text_input("Enter stock ticker symbol", value="AAPL").upper()

if ticker:
    try:
        stock = yf.Ticker(ticker)

        # --- Date Range Picker ---
        st.write("### 📅 Select Date Range")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start date", value=datetime.date(2023, 1, 1))
        with col2:
            end_date = st.date_input("End date", value=datetime.date.today())

        hist = stock.history(start=start_date, end=end_date)
        info = stock.get_info()  # Updated API

        # --- Basic Info ---
        st.subheader(f"{info.get('shortName', ticker)} ({ticker})")
        st.write(f"Sector: {info.get('sector', 'N/A')}")
        st.write(f"Industry: {info.get('industry', 'N/A')}")

        # --- Price Chart ---
        st.write("### 📈 Stock Price Chart")
        if not hist.empty:
            st.line_chart(hist["Close"])
        else:
            st.warning("⚠️ No data available for this date range.")

        # --- Key Financial Metrics ---
        st.write("### 📌 Key Financial Metrics")

        metrics = {
            "Market Cap": info.get("marketCap"),
            "Trailing P/E": info.get("trailingPE"),
            "Forward P/E": info.get("forwardPE"),
            "PEG Ratio": info.get("pegRatio"),
            "Price to Book": info.get("priceToBook"),
            "Profit Margin": info.get("profitMargins"),
            "Return on Equity": info.get("returnOnEquity"),
            "Operating Margin": info.get("operatingMargins"),
            "Debt to Equity": info.get("debtToEquity"),
            "Total Revenue": info.get("totalRevenue"),
            "EBITDA": info.get("ebitda"),
            "Beta": info.get("beta")
        }

        for key, value in metrics.items():
            if value is not None:
                if isinstance(value, float):
                    st.write(f"{key}: {value:.2f}")
                else:
                    st.write(f"{key}: {value}")
            else:
                st.write(f"{key}: N/A")

        # --- Static Synopsis ---
        st.write("### 🧠 Investment Thesis")
        st.info(
            f"{ticker} shows promising financial health with key indicators like strong profit margins, manageable debt, and stable revenue growth. "
            "This could indicate potential for long-term investment depending on market conditions."
        )

        # --- Refresh Button ---
        if st.button("🔄 Refresh Data"):
            st.experimental_rerun()

    except Exception as e:
        st.error(f"❌ Error fetching data for {ticker}: {e}")
else:
    st.info("Please enter a ticker symbol to view stock information.")
