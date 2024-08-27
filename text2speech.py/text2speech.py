import streamlit as st
import os
import base64
from pydub import AudioSegment
from openai import OpenAI, OpenAIError  # Ensure proper imports for error handling
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch API key and other parameters securely
api_key = os.getenv("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")
base_url = "http://api.groq.com/openapi/v1/"

# Ensure API key is not None
if not api_key:
    raise ValueError("API key is missing. Please check your environment variables.")

# Initialize the OpenAI client
try:
    groq = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )
except OpenAIError as e:
    st.error(f"Failed to initialize OpenAI client: {e}")
    st.stop()

llm = AzureChatOpenAI(
    openai_api_version=os.getenv("OPENAI_API_GPT_4_VERSION"),
    azure_deployment="gpt-4o",
    model="gpt-4o",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_GPT_4_KEY"),
    azure_endpoint=os.getenv("OPENAI_API_GPT_4_BASE")
)

def audio_to_base64(file):
    with open(file, "rb") as audio_file:
        audio_bytes = audio_file.read()
        base64_audio = base64.b64encode(audio_bytes).decode()
    return base64_audio

st.set_page_config(
    layout="wide",
    page_title="Speech to Text"
)

st.title("Speech to Text")

uploaded_file = st.file_uploader("Upload an audio file", type=["mp3"])

if uploaded_file is not None:
    with open("uploaded_file.mp3", "wb") as f:
        f.write(uploaded_file.read())

    base64_audio = audio_to_base64("uploaded_file.mp3")
    
    audio_html = f"""
    <audio controls>
        <source src="data:audio/mp3;base64,{base64_audio}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    """
    
    st.subheader("Your uploaded audio file")
    st.markdown(audio_html, unsafe_allow_html=True)
    
    if st.button('Transcribe'):
        try:
            with open("uploaded_file.mp3", "rb") as audio_file:
                transcript = groq.audio.transcriptions.create(
                    model="whisper-large-v3",
                    file=audio_file,
                    response_format="text"
                )
            st.success("Transcribed Text: " + transcript)
        except OpenAIError as e:
            st.error(f"Transcription failed: {e}")
