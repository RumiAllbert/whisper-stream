import tempfile
import threading

import streamlit as st
import whisper
import yaml
from yaml import SafeLoader

from utility import write_srt

MODEL_SIZE = "base.en"
# --------------------------------------------------------------------------------------------------
# Set the page configuration
# --------------------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Transcriber",
    page_icon="🤖",
    layout="wide",
    menu_items={
        "Get Help": "https://studentsforfg.org/",
        "About": """Simple GUI for OpenAI's Whisper.""",
    },
)

# List of languages supported by OpenAI's Whisper
languages = [
    "Auto Detect",
    "Afrikaans",
    "Albanian",
    "Amharic",
    "Arabic",
    "Armenian",
    "Assamese",
    "Azerbaijani",
    "Bashkir",
    "Basque",
    "Belarusian",
    "Bengali",
    "Bosnian",
    "Breton",
    "Bulgarian",
    "Burmese",
    "Castilian",
    "Catalan",
    "Chinese",
    "Croatian",
    "Czech",
    "Danish",
    "Dutch",
    "English",
    "Estonian",
    "Faroese",
    "Finnish",
    "Flemish",
    "French",
    "Galician",
    "Georgian",
    "German",
    "Greek",
    "Gujarati",
    "Haitian",
    "Haitian Creole",
    "Hausa",
    "Hawaiian",
    "Hebrew",
    "Hindi",
    "Hungarian",
    "Icelandic",
    "Indonesian",
    "Italian",
    "Japanese",
    "Javanese",
    "Kannada",
    "Kazakh",
    "Khmer",
    "Korean",
    "Lao",
    "Latin",
    "Latvian",
    "Letzeburgesch",
    "Lingala",
    "Lithuanian",
    "Luxembourgish",
    "Macedonian",
    "Malagasy",
    "Malay",
    "Malayalam",
    "Maltese",
    "Maori",
    "Marathi",
    "Moldavian",
    "Moldovan",
    "Mongolian",
    "Myanmar",
    "Nepali",
    "Norwegian",
    "Nynorsk",
    "Occitan",
    "Panjabi",
    "Pashto",
    "Persian",
    "Polish",
    "Portuguese",
    "Punjabi",
    "Pushto",
    "Romanian",
    "Russian",
    "Sanskrit",
    "Serbian",
    "Shona",
    "Sindhi",
    "Sinhala",
    "Sinhalese",
    "Slovak",
    "Slovenian",
    "Somali",
    "Spanish",
    "Sundanese",
    "Swahili",
    "Swedish",
    "Tagalog",
    "Tajik",
    "Tamil",
    "Tatar",
    "Telugu",
    "Thai",
    "Tibetan",
    "Turkish",
    "Turkmen",
    "Ukrainian",
    "Urdu",
    "Uzbek",
    "Valencian",
    "Vietnamese",
    "Welsh",
    "Yiddish",
    "Yoruba",
]

# --------------------------------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------------------------------
# Create a temporary directory
temp_dir = tempfile.TemporaryDirectory()
st.session_state.transcription = None

# --------------------------------------------------------------------------------------------------
# Page Start
# --------------------------------------------------------------------------------------------------
st.title("✍️ Simple Transcriber")

# Set a h2 header
st.header("Upload an audio file to get started")

# -------------------
# Functions
# -------------------
# Upload an audio file
def load_audio_file(audio_file):
    """Load audio file from specified"""
    if audio_file is None:
        if audio_file := st.file_uploader(
            label="Audio File", type=["mp3", "wav", "m4a", "wma", "aac"]
        ):
            # Store the audio file in the temporary directory
            with open(f"{temp_dir.name}/{audio_file.name}", "wb") as f:
                f.write(audio_file.read())

            return f"{temp_dir.name}/{audio_file.name}"


# semaphore = threading.Semaphore(1)


# @st.experimental_singleton
@st.cache_resource
def load_model(size=MODEL_SIZE):
    """Load whisper model"""
    # Acquire the Semaphore
    # semaphore.acquire()
    try:
        model = whisper.load_model(size)
    except Exception as exp:
        st.error(f"Error loading model.\n{exp}")
        model = None
    finally:
        # Release the Semaphore
        # semaphore.release()
        return model


# Load the model and audio file
audio_file = load_audio_file(None)

# model = load_model()
if "model" not in st.session_state:
    st.session_state["model"] = load_model()
model = st.session_state["model"]


@st.cache_data
def transcribe(audio_file, language):
    """Transcribe the audio file"""
    # Acquire the Semaphore
    # semaphore.acquire()
    try:
        if audio_file is not None:
            with st.spinner("Transcription is currently in progress. Please wait..."):
                st.sidebar.empty()
                st.sidebar.success("Transcribing...")
                transcription = model.transcribe(audio_file, language=language)
                st.session_state.transcription = transcription["text"]
                st.session_state.segments = write_srt(transcription["segments"])
                return transcription["text"]
    finally:
        st.sidebar.success("Transcription complete!")
        # Release the lock
        # semaphore.release()


# If the model and audio file have been loaded, transcribe the audio file
transcription = None
if model is not None and audio_file is not None:
    # h3 header
    st.markdown("#### Press the button to transcribe the audio file")
    language = st.selectbox("🗣️ Select Language", languages)
    # If language is not "Auto Detect", or "English", raise a warning message
    if language not in ["Auto Detect", "English"]:
        st.warning(
            "The language you have selected is not supported by the model. The model will default to English.\n\nIf you would like to use a different language, please contact the developer."
        )
    if language in "Auto Detect":
        language = None
    if model is not None and st.button(
        "Transcribe ✨", type="primary", help="Transcribe the audio file"
    ):
        try:
            # Transcribe the audio file asynchronously
            transcription = transcribe(audio_file, language)
        except Exception as exp:
            # Display a warning message if the semaphore is already in use
            st.warning(
                f"There was an error transcribing the audio file. Please try again. If the problem persists, please contact the developer."
            )
            # print the error
            st.error(exp)

# Add a line break
st.markdown("---")

# --------------------------------------------------------------------------------------------------
# Download the transcription
# --------------------------------------------------------------------------------------------------
# Display the original audio file
if audio_file is not None:
    st.sidebar.header("Play Original Audio File")
    st.sidebar.audio(audio_file)

# Display the transcription
if transcription is not None:
    st.markdown("## Transcription")
    st.write(transcription)

    # Download the transcription as a text file if the audio file has been loaded and the transcription has been completed
    st.markdown("#### Download Transcription")
    st.download_button(
        label="Download .txt",
        data=transcription,
        file_name="transcription.txt",
        mime="text/plain",
    )
    # SRT file
    st.download_button(
        label="Download .srt",
        data=st.session_state.segments,
        file_name="transcription.srt",
        mime="text/plain",
    )

# Clean up the temporary directory
temp_dir.cleanup()

# Add a footer to the main area
st.markdown(
    '<div style="position: fixed; bottom: 0; width: 100%; text-align: center;">'
    'Made with ❤️ by <a href="https://studentsforfg.org/">SFFG</a>'
    "</div>",
    unsafe_allow_html=True,
)
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
