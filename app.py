import streamlit as st
import suitabilitymodel

st.title("Stock Suitability Analysis Model (SSAM)")

ticker = st.text_input("Enter stock symbol (e.g., RELIANCE.NS):", "ITC.NS")

if st.button("Analyze"):
    with st.spinner("Analyzing..."):
        result = suitabilitymodel.generate_trade_signal(ticker)
        forecast = suitabilitymodel.arima_forecast(ticker)
    st.subheader("Analysis Result")
    for key, value in result.items():
        st.write(f"**{key}:** {value}")
    st.subheader("ARIMA Forecast (Next 5 Days)")
    st.write(forecast)