import streamlit as st
import requests

st.title("🚀 AI Study Chatbot (Offline)")

# sidebar
st.sidebar.title("Features")
st.sidebar.write("✔ DSA Help\n✔ DBMS Help\n✔ Interview Prep")

# memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# input
user_input = st.chat_input("Ask anything...")

# function to get response
def get_response(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "tinyllama",
            "prompt": f"""
You are a strict DSA and interview expert.

Rules:
- Answer ONLY what user asks
- Keep answers SHORT and CLEAR
- No extra story or motivation
- If question is outside DSA, answer normally but briefly

User: {prompt}
AI:
""",
            "stream": False
        }
    )
    return response.json().get("response", "Error")

# handle input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    reply = get_response(user_input)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)