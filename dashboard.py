import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="AI Stock Dashboard Demo", layout="wide")

st.title("AI Stock Dashboard Demo")

# Input ticker symbol
ticker = st.text_input("Enter stock ticker symbol", value="AAPL").upper()

if ticker:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")

        # Basic stock info
        info = stock.info
        st.subheader(f"{info.get('shortName', ticker)} ({ticker})")
        st.write(f"Sector: {info.get('sector', 'N/A')}")
        st.write(f"Industry: {info.get('industry', 'N/A')}")

        # Show stock price chart
        st.line_chart(hist['Close'])

        # Financial highlights
        st.write("### Key Financials")
        revenue_growth = info.get('revenueGrowth')
        if revenue_growth:
            st.write(f"Revenue Growth (TTM): {revenue_growth*100:.2f}%")
        else:
            st.write("Revenue Growth data not available.")

        # Dummy synopsis (static text)
        st.write("### Investment Synopsis")
        st.info(
            "This stock has demonstrated steady revenue growth and strong market position. "
            "It shows potential for long-term appreciation based on fundamentals."
        )

        # Refresh button (reloads the app)
        if st.button("Refresh Data"):
            st.experimental_rerun()

    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
else:
    st.info("Please enter a ticker symbol to view stock information.")
