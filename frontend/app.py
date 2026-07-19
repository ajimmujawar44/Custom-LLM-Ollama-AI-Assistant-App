import streamlit as st
from ollama import Client
import os
import time

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Custom LLM Chat",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Ollama Client
# -----------------------------
client = Client(host="http://localhost:11434")

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main{
    padding-top:20px;
}

h1{
    color:#00B4D8;
    text-align:center;
}

.response-box{
    padding:20px;
    border-radius:12px;
    background:#262730;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ===================================
# Sidebar
# ===================================

with st.sidebar:

    from pathlib import Path

    logo_path = Path(__file__).parent / "assets" / "logo.png"

    st.image(str(logo_path), use_container_width=True)
    st.title("AM AI Assistant")

    st.caption("Your Local AI Companion")

    st.divider()

    model = st.selectbox(
        "🧠 Select AI Model",
        [
            "gemma3:270m"
        ]
    )

    st.divider()

    st.success("🟢 Ollama Connected")

    st.divider()

    if st.button("🆕 New Chat"):

        st.session_state.messages = []
        
        st.rerun()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []
        
        st.rerun()
        st.divider()

    st.markdown("### 👨‍💻 Developer")

    st.write("**Azim Mujawar**")

    st.caption("Python | Streamlit | Ollama")

    st.caption("Version 1.0")

# ============================================
# Session State
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================
# Welcome Screen
# ============================================
prompt = st.chat_input("Ask anything...")
# ============================================
# App Header (Always Visible)
# ============================================

st.markdown(
    """
    <div style="text-align:center; margin-top:20px;">

    <h1>🤖 AM AI Assistant</h1>

    <h4>Chat with your Local AI using Ollama</h4>

    <p style="font-size:16px;">
    Generate AI responses completely offline using
    <b>Gemma 3</b>.
    </p>

    <p style="color:gray;">
    ⚡ Fast &nbsp;&nbsp;
    🔒 Private &nbsp;&nbsp;
    💻 Local
    </p>

    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ============================================
# Show Quick Start only before first message
# ============================================
if len(st.session_state.messages) == 0 and prompt is None:

    st.info("""
💡 **Quick Start**

• Explain Machine Learning

• Write Python Code

• SQL Query Example

• Explain Generative AI
""")
# Show Conversation
for message in st.session_state.messages:

    with st.chat_message(message["role"], avatar="🤖" if message["role"]=="assistant" else "👨‍💻"):

        st.markdown(message["content"])
# ============================================
# Chat Input
# ============================================


if prompt:
    st.session_state.chat_started = True
    
    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(prompt)
    start_time = time.time()

    with st.spinner("🤖 Thinking..."):

        response = client.chat(            

            model=model,

            messages=st.session_state.messages

            )
        
        end_time = time.time()

        response_time = round(end_time - start_time, 2)

        answer = response["message"]["content"]

        st.session_state.messages.append(

    {
        "role":"assistant",
        "content":answer
    }

    )               
        with st.chat_message("assistant", avatar="🤖"):

            st.markdown(answer)
            st.caption(f"⚡ Generated in {response_time} sec using {model}")
            st.divider()
            st.caption("© 2026 Azim Mujawar | Built with Streamlit + Ollama")