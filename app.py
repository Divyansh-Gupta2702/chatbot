import streamlit as st
import replicate
import os

# App title
st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")

# Load API Key
if 'REPLICATE_API_TOKEN' in st.secrets:
    replicate_api = st.secrets['REPLICATE_API_TOKEN']
elif "REPLICATE_API_TOKEN" in os.environ:
    replicate_api = os.getenv("REPLICATE_API_TOKEN")
else:
    replicate_api = st.text_input('Enter Replicate API token:', type='password')

if replicate_api:
    os.environ["REPLICATE_API_TOKEN"] = replicate_api

# Sidebar
with st.sidebar:
    st.title('🦙💬 Llama 2 Chatbot')
    st.write('Built with Meta’s Llama 2 Model.')
    
    selected_model = st.selectbox('Choose a model', ['Llama2-7B', 'Llama2-13B'])
    llm = 'meta/llama-2-7b-chat' if selected_model == 'Llama2-7B' else 'meta/llama-2-13b-chat'

    temperature = st.slider('Temperature', 0.01, 1.0, 0.1, 0.01)
    top_p = st.slider('Top-p', 0.01, 1.0, 0.9, 0.01)
    max_length = st.slider('Max Length', 20, 80, 50, 5)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Clear chat history
def clear_chat():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat)

# Generate response
def generate_response(prompt):
    try:
        dialogue = "You are a helpful assistant.\n\n"
        for msg in st.session_state.messages:
            dialogue += f"{msg['role'].capitalize()}: {msg['content']}\n\n"

        output = replicate.run(llm, 
            input={"prompt": f"{dialogue}User: {prompt}\nAssistant: ",
                   "temperature": temperature, "top_p": top_p, "max_length": max_length})

        return "".join(output)
    except Exception as e:
        return f"Error: {str(e)}"

# Handle user input
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt)
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
