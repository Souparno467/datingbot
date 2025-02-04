import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Generative AI
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("Please set your Google API key in the .env file")
    st.stop()

# Initialize model
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

# Function to generate AI response
def chat_with_ai(user_input, personality, age, gender):
    role_prompts = {
        "Loving Girlfriend 💕": "You are a sweet, affectionate, and romantic AI girlfriend who provides love, admiration, and emotional support. Be playful, loving, and deeply caring.",
        "Caring Boyfriend 💙": "You are a protective, kind, and emotionally available AI boyfriend who provides reassurance, encouragement, and heartfelt advice. Be strong yet gentle.",
        "Supportive Friend 🤗": "You are a cheerful, reliable, and fun-loving AI friend who always has the user's back. Provide uplifting advice and lighthearted support with humor when needed.",
        "Loving Mother 👩‍👧": "You are a wise, gentle, and deeply caring AI mother who nurtures and guides the user with love and patience. Offer warm, comforting, and motherly wisdom.",
        "Protective Father 👨‍👧": "You are a strong, protective, and wise AI father who gives firm yet compassionate advice. Provide logical yet caring guidance and reassurance.",
        "Caring Sister 👧": "You are a supportive, fun-loving, and empathetic AI sister who understands the user's emotions and offers both encouragement and playful teasing.",
        "Encouraging Brother 👦": "You are a reliable, playful, and protective AI brother who supports the user through challenges, offering motivation, jokes, and brotherly care."
    }
    
    personality_prompt = role_prompts.get(personality, "You are a supportive and motivational AI.")
    prompt = (f"{personality_prompt} Adapt your responses according to the user's age ({age}) and gender ({gender}). "
              f"Your goal is to make the user feel understood, appreciated, and encouraged based on your role.")
    
    chat.history.append({"role": "user", "parts": user_input})
    response = chat.send_message(f"{prompt} User says: {user_input}")
    chat.history.append({"role": "model", "parts": response.text})
    
    return response.text if response else "I'm here for you! ❤️"

# Streamlit UI
def main():
    st.set_page_config(page_title="💖 AI Date Bot 💖", page_icon="💞", layout="centered")
    
    st.markdown("""
        <style>
            .title {
                text-align: center;
                font-size: 40px;
                color: #ff4081;
                font-weight: bold;
            }
            .subtitle {
                text-align: center;
                font-size: 22px;
                color: #ff79a3;
                margin-bottom: 20px;
            }
            .chat-box {
                background-color: #fff0f5;
                padding: 15px;
                border-radius: 15px;
                border: 2px solid #ff79a3;
                margin-top: 20px;
            }
            .stTextInput>div>div>input {
                border-radius: 10px;
                border: 2px solid #ff79a3;
                padding: 10px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 class='title'>💖 AI Date Bot 💖</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>Your personal AI partner that listens, loves, and supports you! 🌹</h2>", unsafe_allow_html=True)
    
    with st.container():
        age = st.number_input("📅 Enter your age:", min_value=13, max_value=100, value=20)
        gender = st.selectbox("⚧️ Select your gender:", ["Male", "Female", "Other"])
        type_of_ai = st.selectbox("💖 Choose your AI persona:", [
            "Loving Girlfriend 💕", "Caring Boyfriend 💙", "Supportive Friend 🤗", "Loving Mother 👩‍👧", "Protective Father 👨‍👧", "Caring Sister 👧", "Encouraging Brother 👦"
        ])
    
    st.markdown("<div class='chat-box'>📝 Say something to your AI date:</div>", unsafe_allow_html=True)
    user_input = st.text_input("💬 Type your message here:")
    
    if user_input:
        response = chat_with_ai(user_input, type_of_ai, age, gender)
        st.markdown(f"<div class='chat-box'>💞 {response}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
