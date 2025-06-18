import streamlit as st
import yfinance as yf
import datetime
from google import genai
from google.genai import types

# --- Gemini Setup ---
client = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    api_key=st.secrets["GEMINI_API_KEY"]
)
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"],
    http_options=types.HttpOptions(api_version="v1"),
)

# --- Streamlit UI ---
st.set_page_config(page_title="AI Stock Dashboard", layout="centered")
st.title("📊 AI-Powered Stock Dashboard")

ticker = st.text_input("Enter a stock ticker symbol (e.g. AAPL, TSLA, MSFT):", "AAPL")
start_date = st.date_input("Start Date", datetime.date(2023, 1, 1))
end_date = st.date_input("End Date", datetime.date.today())

# --- Gemini Synopsis Generator ---
def generate_synopsis(prompt):
    try:
        response = client.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error generating synopsis: {e}"

# --- Main Logic ---
if ticker:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)

        if hist.empty:
            st.warning("⚠️ No historical data found. Please check the ticker or date range.")
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

            # Build Prompt
            summary_prompt = f"""
You are a financial analyst. Based on the following data for {ticker}, write a clear and concise investment thesis in under 100 words:

- Current Price: {fast_info.get("lastPrice", "N/A")}
- 52-Week High: {fast_info.get("yearHigh", "N/A")}
- 52-Week Low: {fast_info.get("yearLow", "N/A")}
- Market Cap: {fast_info.get("marketCap", "N/A")}
"""

            st.subheader("🧠 AI-Generated Investment Synopsis")
            if st.button("Generate Synopsis"):
                with st.spinner("Analyzing with Gemini..."):
                    synopsis = generate_synopsis(summary_prompt)
                st.success(synopsis)

    except Exception as e:
        st.error(f"❌ Failed to fetch stock data: {e}")
