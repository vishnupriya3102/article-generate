import streamlit as st
import google.generativeai as genai

# 🔐 Set your Gemini API key
genai.configure(api_key="AIzaSyB4IjWrszJ5c50JyBBSSy5CTcgNSvvHQEw")  # Replace with your real key

# 🎯 Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# 🖼️ Streamlit UI
st.title("🌍 English to French Translator using Gemini")
input_text = st.text_input("Enter an English sentence:")

if input_text:
    prompt = f"Translate the following English sentence into French:\n\n{input_text}"
    response = model.generate_content(prompt)
    st.success(response.text)
