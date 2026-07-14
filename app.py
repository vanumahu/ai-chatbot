import streamlit as st
import requests

API_KEY = st.secrets["API_KEY"]
url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

CV_CONTEXT = """ 
[KEEP YOUR EXISTING CV_CONTEXT HERE — unchanged]
"""

st.title("🤖 Vani's AI Chatbot")

# ------------------------
# SESSION STATE
# ------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------
# 👇 SUGGESTED PROMPTS (NEW)
# ------------------------
if len(st.session_state.messages) == 0:
    st.markdown("### 👋 Start here")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✨ Professional Summary"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Tell me about yourself"
            })
            st.rerun()

    with col2:
        if st.button("Experience at 3M"):
            st.session_state.messages.append({
                "role": "user",
                "content": "What did you do at 3M?"
            })
            st.rerun()

    with col3:
        if st.button("Key Skills"):
            st.session_state.messages.append({
                "role": "user",
                "content": "What are your key skills?"
            })
            st.rerun()

# ------------------------
# DISPLAY CHAT HISTORY
# ------------------------
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ------------------------
# FUNCTION TO CALL API (NEW - CLEANER)
# ------------------------
def get_response():
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": CV_CONTEXT}
        ] + st.session_state.messages
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

# ------------------------
# HANDLE BUTTON-TRIGGERED MESSAGE (NEW)
# ------------------------
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_user_msg = st.session_state.messages[-1]["content"]

    # Avoid duplicate assistant responses
    if len(st.session_state.messages) == 1 or st.session_state.messages[-2]["role"] != "assistant":
        reply = get_response()

        st.chat_message("assistant").write(reply)

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })

# ------------------------
# CHAT INPUT
# ------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    st.chat_message("user").write(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    reply = get_response()

    st.chat_message("assistant").write(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
