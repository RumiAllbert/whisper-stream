import streamlit as st
import whisper

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

st.session_state.transcription = None

st.title("Simple Transcriber")

# Set a h2 header
st.header("Upload an audio file to get started")

# Upload an audio file
# @st.cache(show_spinner=True, allow_output_mutation=True, suppress_st_warning=True)
def load_audio_file(audio_file):
    if audio_file is None:
        audio_file = st.file_uploader("Upload", type=["mp3", "wav", "m4a"])
    return audio_file


audio_file = load_audio_file(None)

# Load the model
@st.cache(suppress_st_warning=True)
def load_model():
    try:
        return whisper.load_model("base")
    except Exception as e:
        st.error(
            "There was an error loading the model. Please contact [email](mailto:youngpractitioners.group@gmail.com) to report this issue."
        )


model = load_model()

# Transcribe the audio file
@st.cache(suppress_st_warning=True, allow_output_mutation=True, show_spinner=True)
def transcribe(audio_file, model):
    if audio_file is not None:
        st.sidebar.empty()
        st.sidebar.success("Transcribing...")
        transcription = model.transcribe(audio_file.name)
        st.sidebar.success("Transcription complete!")
        st.session_state.transcription = transcription["text"]
        return transcription["text"]


# If the model and audio file have been loaded, transcribe the audio file
transcription = None
if model is not None and audio_file is not None:
    # h3 header
    st.markdown("#### Press the button to transcribe the audio file")
    if model is not None and st.button(
        "Transcribe", type="primary", help="Transcribe the audio file"
    ):
        transcription = transcribe(audio_file, model)

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
    st.markdown("#### Download the transcription as a text file")
    st.download_button(
        label="Download transcription",
        data=transcription,
        file_name="transcription.txt",
        mime="text/plain",
    )
