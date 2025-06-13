import streamlit as st
import google.generativeai as genai
import datetime

# 💡 Set your Gemini API key (store it securely in secrets for production)
genai.configure(api_key="AIzaSyD-HSB0UIMx3uZ4an-X5BedRNwPTMKXX6o")  # replace with st.secrets["GEMINI_API_KEY"]

# 🔧 Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash-001')

# 🧠 Streamlit UI
st.title("📝 AI Article Generator using Gemini")
st.subheader("Create engaging articles in seconds!")

st.sidebar.header("Customize Your Article")

# 📌 User Inputs
topic = st.sidebar.text_input("Enter the topic", "Impact of AI on Jobs")
tone = st.sidebar.selectbox("Select tone", ["Formal", "Informal", "Persuasive", "Creative", "Professional"])
length = st.sidebar.slider("Article length (words)", 100, 1500, 500)

# Extra options
add_summary = st.sidebar.checkbox("Include a summary at the end", value=True)
add_keywords = st.sidebar.checkbox("Extract keywords", value=False)

# ✨ Generate Article
if st.sidebar.button("Generate Article"):
    with st.spinner("Generating your article with Gemini..."):

        # 🔥 Compose prompt
        gemini_prompt = f"""
        Write a {tone.lower()} article about "{topic}" in approximately {length} words.
        Structure it with a strong introduction, body paragraphs, and conclusion.
        {'Include a brief summary at the end.' if add_summary else ''}
        {'Also extract 5–10 relevant keywords at the end in a bullet list.' if add_keywords else ''}
        """

        # 📡 Call Gemini
        response = model.generate_content(gemini_prompt)
        article = response.text

        # ✅ Display result
        st.success("Article Generated!")
        st.markdown(article)

        # 📥 Download
        file_name = f"{topic.replace(' ', '_')}_article.txt"
        st.download_button("📩 Download Article", article, file_name=file_name)

# Footer
st.markdown("---")
st.markdown("🚀 Built with [Gemini AI](https://ai.google.dev) & Streamlit | 🔒 Keep your API key secure")
st.caption(f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
