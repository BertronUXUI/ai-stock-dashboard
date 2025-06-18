import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="AI Stock Dashboard Demo", layout="wide")
st.title("📊 AI Stock Dashboard Demo")

# Input ticker symbol
ticker = st.text_input("Enter stock ticker symbol", value="AAPL").upper()

if ticker:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        info = stock.get_info()  # Updated to avoid deprecated .info

        # Basic stock info
        st.subheader(f"{info.get('shortName', ticker)} ({ticker})")
        st.write(f"Sector: {info.get('sector', 'N/A')}")
        st.write(f"Industry: {info.get('industry', 'N/A')}")

        # Show stock price chart
        st.write("### 📈 1-Month Closing Price")
        st.line_chart(hist["Close"])

        # Expanded Key Financial Metrics
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

        # Static/dummy AI-generated synopsis
        st.write("### 🧠 Investment Synopsis")
        st.info(
            f"{ticker} shows promising financial health with key indicators like steady earnings and low debt-to-equity. "
            "Its market fundamentals suggest a potential long-term growth opportunity, especially in current market conditions."
        )

        # Refresh button to reload data
        if st.button("🔄 Refresh Data"):
            st.experimental_rerun()

    except Exception as e:
        st.error(f"❌ Error fetching data for {ticker}: {e}")
else:
    st.info("Please enter a ticker symbol to view stock information.")
