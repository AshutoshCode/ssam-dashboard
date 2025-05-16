import streamlit as st
import suitabilitymodel

st.title("Stock Suitability Analysis Model (SSAM)")

ticker = st.text_input("Enter stock symbol (e.g., RELIANCE.NS):", "ITC.NS")

if st.button("Analyze"):
    with st.spinner("Analyzing..."):
        result = suitabilitymodel.generate_trade_signal(ticker)
    st.subheader("Analysis Result")
    for key, value in result.items():
        st.write(f"**{key}:** {value}")