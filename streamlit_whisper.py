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
audio_file = st.file_uploader("Upload", type=["mp3", "wav", "m4a"])

# Load the model if there is an error loading the model, display an error message to contact the developer
try:
    model = whisper.load_model("base")
except:
    st.error(
        "There was an error loading the model. Please contact [email](mailto:youngpractitioners.group@gmail.com) to report this issue."
    )

# h3 header
st.markdown("#### Press the button to transcribe the audio file")

# Transcribe the audio file
if st.button("Transcribe", type="primary", help="Transcribe the audio file"):
    if audio_file is not None:
        st.sidebar.success("Transcribing...")
        transcription = model.transcribe(audio_file.name)
        st.sidebar.success("Transcription complete!")
        st.session_state.transcription = transcription["text"]
    else:
        st.sidebar.error("Please upload an audio file to get started")

# Display the transcription
if st.session_state.transcription is not None:
    st.markdown("## Transcription")
    st.markdown(st.session_state.transcription)

# Clear the transcription
if st.session_state.transcription is not None:
    if st.button("Clear transcription"):
        st.session_state.transcription = None

st.sidebar.header("Play Original Audio File")
st.sidebar.audio(audio_file)


# Download the transcription as a text file if the audio file has been loaded and the transcription has been completed
if audio_file is not None and st.session_state.transcription is not None:
    st.sidebar.markdown("#### Download the transcription as a text file")
    st.sidebar.download_button(
        label="Download",
        data=st.session_state.transcription,
        file_name="transcription.txt",
        mime="text/plain",
    )
