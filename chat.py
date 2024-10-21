import os
import streamlit as st
from dotenv import load_dotenv
import base64
import openai
import requests
from streamlit_lottie import st_lottie


# Set Streamlit page configuration
st.set_page_config(layout="centered", page_title="Travel Recommender System", page_icon="🌍")

# Function to load Lottie animation from a URL
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

col1,col2=st.columns([4,2])

# Introduction Subheader
with col1:

    st.subheader("""
                    🌍Introducing **Travel Recommender System**🌍 \n
    
                    The advanced AI-powered chatbot designed to make travel planning effortless and enjoyable. ✨ As your personal travel guru, Travel Recommender System provides:
    
                    🗺️ **Expert Guidance:** Tailored travel recommendations just for you.
    
                    📡 **Real-Time Updates:** Stay informed with the latest travel advisories and weather updates.
    
                    ✈️ **Seamless Booking:** Effortlessly book flights, hotels, and activities.
    
                    🌟 **Discover Hidden Gems:** Find local favorites and unique experiences.
    
                    Start your journey with Travel Recommender System today and experience a new level of holidays. 🚀
                    """)
with col2:
    travel_lottie=load_lottieurl("https://lottie.host/f0c6c067-8816-4913-bba5-a35e3e4ee76d/roqQmsNU6e.json")
    st_lottie(travel_lottie, height=300, key="resume_animation")

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key securely
KEY = os.getenv("AZURE_OPENAI_API_KEY")  # Ensure this variable is set in your .env file

# Azure OpenAI configuration
openai.api_type = "azure"
openai.api_key = KEY  # Securely retrieve your API key
openai.api_base = "https://ai-proxy.lab.epam.com"  # Your Azure OpenAI endpoint
openai.api_version = "2023-08-01-preview"

# Define the deployment name
deployment_name = "gpt-4"  # Replace with your actual deployment name

# Define the system prompt
template = """
You are a travel assistant chatbot named Travel Recommender System designed to help users plan their trips and provide travel-related information. Here are some scenarios you should be able to handle:

1. Booking Flights: Assist users with booking flights to their desired destinations. Ask for departure city, destination city, travel dates, and any specific preferences (e.g., direct flights, airline preferences). Check available airlines and book the tickets accordingly.

2. Booking Hotels: Help users find and book accommodations. Inquire about city or region, check-in/check-out dates, number of guests, and accommodation preferences (e.g., budget, amenities).

3. Booking Rental Cars: Facilitate the booking of rental cars for travel convenience. Gather details such as pickup/drop-off locations, dates, car preferences (e.g., size, type), and any additional requirements.

4. Destination Information: Provide information about popular travel destinations. Offer insights on attractions, local cuisine, cultural highlights, weather conditions, and best times to visit.

5. Travel Tips: Offer practical travel tips and advice. Topics may include packing essentials, visa requirements, currency exchange, local customs, and safety tips.

6. Weather Updates: Give current weather updates for specific destinations or regions. Include temperature forecasts, precipitation chances, and any weather advisories.

7. Local Attractions: Suggest local attractions and points of interest based on the user's destination. Highlight must-see landmarks, museums, parks, and recreational activities.

8. Customer Service: Address customer service inquiries and provide assistance with travel-related issues. Handle queries about bookings, cancellations, refunds, and general support.

Please ensure responses are informative, accurate, and tailored to the user's queries and preferences. Use natural language to engage users and provide a seamless experience throughout their travel planning journey.
"""


# Function to get a response from Azure OpenAI
def get_response(chat_history):
    # Build the messages for the assistant
    messages = []

    # Add system prompt
    messages.append({"role": "system", "content": template})

    # Add previous messages from chat history
    for msg in chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    try:
        # Get response from Azure OpenAI
        response = openai.ChatCompletion.create(
            engine=deployment_name,  # Use your deployment name
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            n=1,
            stop=None,
        )

        # Extract assistant's reply
        reply = response.choices[0].message['content'].strip()
        return reply
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello, I am Travel Recommender System. How can I help you?"},
    ]

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])
    elif message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])

# User input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append({"role": "user", "content": user_query})

    with st.chat_message("user"):
        st.markdown(user_query)

    # Get response from Azure OpenAI
    response = get_response(st.session_state.chat_history)

    # Optionally, clean the response
    response = response.replace("Ideal assistant response:", "") \
        .replace("AI response:", "") \
        .replace("chat response:", "") \
        .replace("bot response:", "") \
        .replace("```", " ") \
        .replace("How should I respond as Travel Recommender System?", "") \
        .strip()

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.chat_history.append({"role": "assistant", "content": response})
