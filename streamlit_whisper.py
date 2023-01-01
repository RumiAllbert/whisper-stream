import tempfile


import streamlit as st
import whisper
from utility import write_srt

# Set app wide config
st.set_page_config(
    page_title="Transcriber",
    page_icon="🤖",
    layout="wide",
    menu_items={
        "Get Help": "https://studentsforfg.org/",
        "About": """Simple GUI for OpenAI's Whisper.""",
    },
)


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

# Create a temporary directory
temp_dir = tempfile.TemporaryDirectory()

# Constants
st.session_state.transcription = None

st.title("✍️ Simple Transcriber")

# Set a h2 header
st.header("Upload an audio file to get started")

# Upload an audio file
# @st.cache(show_spinner=True, allow_output_mutation=True, suppress_st_warning=True)
def load_audio_file(audio_file):
    if audio_file is None:
        audio_file = st.file_uploader("Upload", type=["mp3", "wav", "m4a", "wma"])

        if audio_file:
            # Store the audio file in the temporary directory
            with open(f"{temp_dir.name}/{audio_file.name}", "wb") as f:
                f.write(audio_file.read())

            return f"{temp_dir.name}/{audio_file.name}"

        # return audio_file


audio_file = load_audio_file(None)
# Load the model
@st.cache(suppress_st_warning=True)
def load_model():
    try:
        return whisper.load_model("base")
    except Exception as LoadModelError:
        st.error(
            "There was an error loading the model. Please contact [email](mailto:youngpractitioners.group@gmail.com) to report this issue."
        )


model = load_model()

# Transcribe the audio file
@st.cache(suppress_st_warning=True, allow_output_mutation=True, show_spinner=True)
def transcribe(audio_file, model, language):
    if audio_file is not None:
        st.sidebar.empty()
        st.sidebar.success("Transcribing...")
        transcription = model.transcribe(audio_file, language=language)
        st.sidebar.success("Transcription complete!")
        st.session_state.transcription = transcription["text"]
        st.session_state.segments = write_srt(transcription["segments"])
        return transcription["text"]


# If the model and audio file have been loaded, transcribe the audio file
transcription = None
if model is not None and audio_file is not None:
    # h3 header
    st.markdown("#### Press the button to transcribe the audio file")
    language = st.selectbox("🗣️ Select Language", languages)
    if language in "Auto Detect":
        language = None
    if model is not None and st.button(
        "Transcribe", type="primary", help="Transcribe the audio file"
    ):
        transcription = transcribe(audio_file, model, language)

    # Add a line break
    st.markdown("---")

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
