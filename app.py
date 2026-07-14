import streamlit as st
import requests

API_KEY = st.secrets["API_KEY"]
url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

st.title("🤖 Vani's AI Chatbot")

# store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# input box
user_input = st.chat_input("Type your message...")

if user_input:
    st.chat_message("user").write(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": st.session_state.messages
    }

    response = requests.post(url, headers=headers, json=data)

    reply = response.json()["choices"][0]["message"]["content"]

    st.chat_message("assistant").write(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
