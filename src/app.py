import tempfile

import streamlit as st
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

from config import set_page_config
from constants import languages
from utility import write_srt
from model import initialize_pipe

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3"

# --------------------------------------------------------------------------------------------------
# Set the page configuration
# --------------------------------------------------------------------------------------------------
set_page_config()

# Init the pipeline
pipe = initialize_pipe(
    model_id=model_id,
    torch_dtype=torch_dtype,
    device=device,
)

# --------------------------------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------------------------------
# Create a temporary directory
temp_dir = tempfile.TemporaryDirectory()
st.session_state.transcription = None
st.session_state.chunks = None

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
        audio_file = st.file_uploader(
            label="Audio File", type=["mp3", "wav", "m4a", "wma", "aac"]
        )
        if audio_file:
            try:
                # Pass the file object directly to the load_model function if possible
                return audio_file
            except Exception as e:
                st.error(f"Error loading audio file.\n{e}")
    return None


# Load the model and audio file
audio_file = load_audio_file(None)


@st.cache_data
def transcribe(audio_file, language):
    """Transcribe the audio file"""
    try:
        if audio_file is not None:
            with st.spinner("Transcription is currently in progress. Please wait..."):
                st.sidebar.empty()
                st.sidebar.success("Transcribing...")

                # # Save the uploaded file to a temporary location
                temp_file = tempfile.NamedTemporaryFile(delete=False)
                temp_file.write(audio_file.getvalue())
                temp_file.close()

                # # Load the audio file
                # dataset = load_dataset(temp_file.name, "clean", split="validation")
                # sample = dataset[0]["audio"]

                # Transcribe the audio file
                if language is not None:
                    result = pipe(
                        temp_file.name, generate_kwargs={"language": language.lower()}
                    )
                else:
                    result = pipe(temp_file.name)

                print(result)

                st.session_state.transcription = result["text"]
                # st.session_state.chunks = write_srt(result["chunks"])
                st.session_state.chunks = result["chunks"]
                return result["text"]
    except Exception as e:
        st.error(f"Error occurred during transcription: {e}")
    finally:
        st.sidebar.success("Transcription complete!")


if audio_file is not None:
    # Display a header for the transcription button
    st.markdown("#### Press the button to transcribe the audio file")

    # Select the language
    language = st.selectbox("🗣️ Select Language", languages)

    # Display a warning if the selected language is not supported
    if language not in ["Auto Detect", "English"]:
        st.warning(
            "The language you have selected is not supported by the model. The model will default to English.\n\nIf you would like to use a different language, please contact the developer."
        )

    # Set language to None if "Auto Detect" is selected
    if language == "Auto Detect":
        language = None

    # Transcribe the audio file when the button is clicked
    if st.button("Transcribe ✨", type="primary", help="Transcribe the audio file"):
        try:
            # Transcribe the audio file asynchronously
            # TODO include language detection
            # ! Currently only English will be suported for this model
            transcription = transcribe(audio_file, language)
        except Exception as exp:
            # Display an error message if there is an error during transcription
            st.warning(
                "There was an error transcribing the audio file. Please try again. If the problem persists, please contact the developer."
            )
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
if st.session_state.transcription is not None:
    st.markdown("## Transcription")
    st.write(st.session_state.transcription)

    # Download the transcription as a text file if the audio file has been loaded and the transcription has been completed
    st.markdown("#### Download Transcription")
    st.download_button(
        label="Download .txt",
        data=st.session_state.transcription,
        file_name="transcription.txt",
        mime="text/plain",
    )
    # SRT file
    st.download_button(
        label="Download .srt",
        data=st.session_state.chunks,
        file_name="transcription.srt",
        mime="text/plain",
    )

# Clean up the temporary directory
temp_dir.cleanup()
