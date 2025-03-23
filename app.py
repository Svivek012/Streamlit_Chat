import streamlit as st
import requests

def chat_interface():
    st.title("Real Estate Bot")
    backend_url = "https://svivek.pythonanywhere.com/webhook"  # Replace with your API URL
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    user_input = st.chat_input("Type your message...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        response = requests.post(backend_url, json={"message": user_input})
        
        if response.status_code == 200:
            try:
                bot_reply = response.json().get("reply", "No response received.")
            except requests.exceptions.JSONDecodeError:
                bot_reply = "Error: Invalid JSON response from server."
        else:
            bot_reply = f"Error {response.status_code}: Could not get a response."
        
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

if __name__ == "__main__":
    chat_interface()
