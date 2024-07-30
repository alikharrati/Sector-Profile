import openai
import streamlit as st
import os

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize the Streamlit session state if not already initialized
if 'messages' not in st.session_state:
    st.session_state.messages = []

def chat_gpt(prompt):
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Create a chat completion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )
    
    # Extract and display the assistant's response
    assistant_message = response.choices[0].message['content'].strip()
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    st.chat_message("assistant").write(assistant_message)

# Streamlit interface
st.title("Chat with GPT-3.5-turbo")
prompt = st.text_input("You: ", key="user_input")

if st.button("Send"):
    if prompt:
        chat_gpt(prompt)

