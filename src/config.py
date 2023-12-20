import pathlib
import streamlit as st

APP_DIR = pathlib.Path(__file__).parent.absolute()

LOCAL_DIR = APP_DIR / "local"
LOCAL_DIR.mkdir(exist_ok=True)


# src/config.py
def set_page_config():
    st.set_page_config(
        page_title="Transcriber",
        page_icon="🤖",
        layout="wide",
        menu_items={
            "Get Help": "https://studentsforfg.org/",
            "About": """Simple GUI for OpenAI's Whisper.""",
        },
    )
