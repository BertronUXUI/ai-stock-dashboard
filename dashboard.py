import streamlit as st
import yfinance as yf
import datetime
from openai import OpenAI

# Set up OpenAI client securely
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📊 AI-Powered Stock Dashboard")

ticker = st.text_input("Enter a stock ticker (e.g., AAPL):", "AAPL")
start_date = st.date_input("Start Date", datetime.date(2023, 1, 1))
end_date = st.date_input("End Date", datetime.date.today())

try:
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=end_date)

    if hist.empty:
        st.warning("⚠️ No historical data found.")
    else:
        st.subheader("📈 Stock Price Chart")
        st.line_chart(hist["Close"])

        fast_info = stock.fast_info
        st.subheader("📌 Key Financial Metrics")
        st.write({
            "Current Price": fast_info.get("lastPrice", "N/A"),
            "52-Week High": fast_info.get("yearHigh", "N/A"),
            "52-Week Low": fast_info.get("yearLow", "N/A"),
            "Market Cap": fast_info.get("marketCap", "N/A")
        })

        st.subheader("🧠 AI-Generated Investment Thesis")
        summary_prompt = f"""
        You are a financial analyst. Based on the following data for {ticker}, write a concise 100-word investment thesis:

        - Current Price: {fast_info.get("lastPrice", "N/A")}
        - 52-Week High: {fast_info.get("yearHigh", "N/A")}
        - 52-Week Low: {fast_info.get("yearLow", "N/A")}
        - Market Cap: {fast_info.get("marketCap", "N/A")}
        """

        if st.button("Generate Synopsis"):
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a financial analyst."},
                        {"role": "user", "content": summary_prompt}
                    ]
                )
                synopsis = response.choices[0].message.content
                st.success(synopsis)
            except Exception as e:
                st.error(f"❌ Error generating synopsis: {e}")

except Exception as e:
    st.error(f"❌ Failed to fetch stock data: {e}")
