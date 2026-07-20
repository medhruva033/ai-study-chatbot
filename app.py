import streamlit as st
import requests

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="AI Study Chatbot",
    page_icon="🚀",
)

st.title("🚀 AI Study Chatbot (Offline)")
st.write("Ask questions about DSA, DBMS, or interview preparation.")

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("Features")
st.sidebar.markdown("""
- ✔ DSA Help
- ✔ DBMS Help
- ✔ Interview Preparation
- ✔ Offline AI using TinyLLaMA
""")

# -------------------------------
# Chat Memory
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------
# Function to Get AI Response
# -------------------------------
def get_response(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": f"""
You are an expert tutor for Data Structures & Algorithms, DBMS, and technical interview preparation.

Rules:
- Answer only the user's question.
- Keep answers short and clear.
- Use examples when helpful.
- If the question is unrelated, answer briefly.

User: {prompt}
Assistant:
""",
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()

        return response.json().get("response", "No response generated.")

    except requests.exceptions.ConnectionError:
        return "❌ Ollama is not running. Start it using `ollama serve`."

    except requests.exceptions.Timeout:
        return "⏳ Request timed out."

    except Exception as e:
        return f"⚠️ Error: {e}"

# -------------------------------
# User Input
# -------------------------------
user_input = st.chat_input("Ask anything...")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        reply = get_response(user_input)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.markdown(reply)
