import streamlit as st
import requests
import uuid

st.title("🤖 AI Customer Support")

# Requirement 32: Unique Session Tracking
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Backend API (Requirement 30)
    response = requests.post(
        "http://localhost:8000/chat", 
        json={"message": prompt, "session_id": st.session_state.session_id}
    )
    
    bot_msg = response.json()["bot_response"]
    
    with st.chat_message("assistant"):
        st.markdown(bot_msg)
    st.session_state.messages.append({"role": "assistant", "content": bot_msg})