import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Gemini 2.0 Flash Chat",
    page_icon="🤖",
    layout="wide"
)

st.title("Gemini 2.0 Flash Chatbot")
st.write("Ask anything and get a response from Gemini 2.0 Flash!")

# Get API key from .env or Streamlit secrets
def get_api_key():
    return os.getenv("GOOGLE_API_KEY")

API_KEY = get_api_key()
if not API_KEY:
    st.error("GOOGLE_API_KEY is not set. Please add it to your environment variables or .env file.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
