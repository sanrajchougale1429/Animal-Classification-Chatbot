from dotenv import load_dotenv
load_dotenv()  # Loading all the environment variables

import os
import google.generativeai as genai

# Configure the API key for the Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")

# Function to get responses from the Gemini AI with a custom prompt
def get_gemini_response(animal_name):
    # Define the prompt
    prompt = f"The following animal species is being checked for its legality in India: {animal_name}. \
    Based on Indian wildlife protection laws and conservation status, respond whether the animal is legal or illegal to own or trade. \
    If it’s not known, mention that too. Provide a brief and precise answer."

    # Generate the response using the model
    response = model.generate_content(prompt)

    # Return the response text
    return response.text

# Console-based input/output
def main():
    print("🐱 Animal Classification Chatbot 🐒")
    input_animal = input("Enter the name of an animal: ")
    
    if input_animal:
        response = get_gemini_response(input_animal)
        print("Response: ", response)
    else:
        print("Please enter an animal name.")

if __name__ == "__main__":
    main()
