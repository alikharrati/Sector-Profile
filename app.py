import openai
import streamlit as st
import os

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Check if the API key is set correctly
if not openai.api_key:
    st.error("OpenAI API key is not set. Please configure the environment variable.")
else:
    st.success("OpenAI API key is set successfully.")

# Initialize the Streamlit session state if not already initialized
if 'messages' not in st.session_state:
    st.session_state.messages = []

def chat_gpt(prompt):
    try:
        # Append user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.write(f"User: {prompt}")
        
        # Create a chat completion
        response = openai.Chat.Completion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        
        # Extract and display the assistant's response
        assistant_message = response.choices[0].message['content'].strip()
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        st.write(f"Assistant: {assistant_message}")
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Streamlit interface
st.title("Chat with GPT-3.5-turbo")
prompt = st.text_input("You: ", key="user_input")

if st.button("Send"):
    if prompt:
        chat_gpt(prompt)
