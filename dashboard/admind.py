import streamlit as st
import requests

API = "http://127.0.0.1:5000/analyze"

st.title("Fake News Explainability Dashboard")

text = st.text_area("Enter News Article")

source = st.text_input("News Source")

if st.button("Analyze Article"):

    payload = {
        "text": text,
        "source": source
    }

    response = requests.post(API, json=payload)

    result = response.json()

    st.subheader("Prediction")
    st.write(result["prediction"])

    st.subheader("Suspicious Claims")
    st.write(result["suspicious_phrases"])

    st.subheader("Explanation")
    st.write(result["explanation"])

    st.subheader("Source Trusted")
    st.write(result["trusted_source"])

    st.subheader("System Metrics")
    st.write(result["metrics"])
    