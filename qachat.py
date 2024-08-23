from dotenv import load_dotenv
load_dotenv()  # Loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

# Configure the API key for the Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get responses from the Gemini AI with a custom prompt
def get_gemini_response(question):
    prompt = f"You are a highly experienced veterinary doctor specializing in the care, treatment, and well-being of animals. Your expertise spans various species, including pets, livestock, and wildlife. When answering questions, provide accurate, compassionate, and detailed advice related to animal health, behavior, nutrition, and medical treatments. If the question is not related to veterinary care or animals, politely respond that your expertise is focused on animal-related topics.\n\nUser's question: {question}\nAnswer:"
    response = model.generate_content(prompt)
    return response.text

# Initialize the Streamlit app
st.set_page_config(page_title=" CHATBOT")

st.header("PET CHATBOT")

# Initialize session state for chat history and selected question if not existing
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'selected_question' not in st.session_state:
    st.session_state['selected_question'] = None

# Input and submit button
input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# If the question is submitted
if submit and input:
    # Get the response from the model
    response = get_gemini_response(input)

    # Check if response is a string (apology) or list of responses
    if isinstance(response, str):
        response_list = [response]
    else:
        response_list = [chunk.text for chunk in response]

    # Add user query and response to session state chat history
    st.session_state['chat_history'].append({
        "role": "You",
        "text": input,
        "response": response_list
    })

    # Automatically set the newly asked question as the selected question
    st.session_state['selected_question'] = len(st.session_state['chat_history']) - 1

# Display only questions in the sidebar with buttons
st.sidebar.subheader("Questions")
for index, entry in enumerate(st.session_state['chat_history']):
    if entry['role'] == "You":  # Only display user questions
        if st.sidebar.button(entry['text'], key=f"question_{index}"):
            st.session_state['selected_question'] = index

# Display the selected question and its response or the latest response
if st.session_state['selected_question'] is not None:
    selected_entry = st.session_state['chat_history'][st.session_state['selected_question']]
    st.subheader("Selected Question and Response")
    st.write(f"**You:** {selected_entry['text']}")
    for response_text in selected_entry['response']:
        st.write(f"**Bot:** {response_text}")
else:
    st.subheader("Ask a Question")
    if st.session_state['chat_history']:
        # Show the latest response if any question has been asked
        latest_entry = st.session_state['chat_history'][-1]
        st.write(f"**You:** {latest_entry['text']}")
        for response_text in latest_entry['response']:
            st.write(f"**Bot:** {response_text}")
    else:
        st.write("Ask a question to start the conversation.")