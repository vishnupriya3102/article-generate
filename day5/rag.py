import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import tempfile
import os

# 🔑 Gemini API Key
GOOGLE_API_KEY = "AIzaSyB4IjWrszJ5c50JyBBSSy5CTcgNSvvHQEw"  # Replace with your key or use st.secrets

# --- 🎨 Streamlit App UI ---
st.set_page_config(page_title="📚 Chat with your PDF", layout="centered")
st.title("📄 Yoo!Upload PDF + Chat (Gemini with Memory)")
st.caption("Ask questions from your uploaded PDF document. Powered by Google Gemini and LangChain.")

# --- 📤 Upload PDF File ---
uploaded_file = st.file_uploader("📁 Upload a PDF file", type=["pdf"])

# --- 💬 Initialize chat history ---
if "chat_history_display" not in st.session_state:
    st.session_state.chat_history_display = []

# --- 💬 Text input for questions ---
user_query = st.text_input("💬 Ask a question about the uploaded document:")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        pdf_path = tmp_file.name

    # --- 📄 Load and split PDF ---
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    # --- 🔍 Create FAISS vector store ---
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )
    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)

    # --- 🤖 Gemini LLM setup ---
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3
    )

    # --- 💬 Chat memory ---
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # --- 🔗 RAG QA Chain ---
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )

    # --- ✅ Handle user query ---
    if user_query:
        response = qa_chain({"question": user_query})
        answer = response["answer"]

        # Save to session_state for persistent history
        st.session_state.chat_history_display.append(("You", user_query))
        st.session_state.chat_history_display.append(("Gemini", answer))

        # Clear temp file
        os.remove(pdf_path)

    # --- 🧠 Display full chat history (chat style) ---
    st.subheader("🧠 Chat History")
    for role, message in st.session_state.chat_history_display:
        if role == "You":
            st.markdown(f"**👤 You:** {message}")
        else:
            st.markdown(f"**🤖 Gemini:** {message}")

else:
    st.info("📥 Please upload a PDF file to begin.")
