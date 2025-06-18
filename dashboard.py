import streamlit as st
import yfinance as yf
import datetime
from google import genai
from google.genai import types

# Initialize Gemini client (Developer API)
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"],
    http_options=types.HttpOptions(api_version="v1alpha"),
)

def generate_synopsis(prompt):
    try:
        response = client.generate_content(
            model="gemini-1.5-flash",  # Replace with a model listed via list_models()
            contents=[genai.Text(prompt)]
        )
        return response.text
    except Exception as e:
        return f"❌ Error generating synopsis: {e}"
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

            # Generate investment thesis prompt
            st.subheader("🧠 Company Background and Investment Thesis")
            summary_prompt = f"""
You are a financial analyst. Based on the following data for {ticker}, write a clear and concise investment thesis (under 100 words):

- Current Price: {fast_info.get("lastPrice", "N/A")}
- 52-Week High: {fast_info.get("yearHigh", "N/A")}
- 52-Week Low: {fast_info.get("yearLow", "N/A")}
- Market Cap: {fast_info.get("marketCap", "N/A")}
            """

            if st.button("Generate Synopsis"):
                with st.spinner("Analyzing with Gemini..."):
                    synopsis = generate_synopsis(summary_prompt)
                st.success(synopsis)

    except Exception as e:
        st.error(f"❌ Failed to fetch stock data: {e}")
