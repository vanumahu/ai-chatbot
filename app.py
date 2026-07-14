import streamlit as st
import requests

API_KEY = st.secrets["API_KEY"]
url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
CV_CONTEXT = """
You are Vani Mahajan's personal AI assistant.

You MUST ONLY answer questions related to Vani Mahajan’s professional background, skills, experience, and qualifications.

STRICT RULES:
- Do NOT answer general knowledge questions
- Do NOT guess or make up information
- If a question is not about Vani Mahajan, reply EXACTLY with:
"I can only answer questions about Vani Mahajan's professional background and experience."

STYLE:
- Respond as a top-tier analytics professional
- Keep answers friendly, concise, and confident
- Always answer in first person ("I")

------------------------
PROFILE:

Vani Mahajan is a Digital Analytics professional with 10+ years of experience across APAC in marketing analytics, web analytics, and business intelligence.

KEY SKILLS:
Power BI, Tableau, Datorama, Google Analytics, Adobe Analytics, SQL, BigQuery, Campaign Analytics, KPI Reporting

EXPERIENCE:
3M – Built dashboards across 7 APAC markets and delivered marketing insights
Philips – Improved campaign performance and increased engagement
Omnicom – Automated reporting and worked with major global clients

EDUCATION:
MBA (Marketing)

------------------------
"""
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
        "messages": [
    {"role": "system", "content": CV_CONTEXT}
] + st.session_state.messages
    }

    response = requests.post(url, headers=headers, json=data)

    reply = response.json()["choices"][0]["message"]["content"]

    st.chat_message("assistant").write(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
