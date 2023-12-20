import pathlib
import streamlit as st

APP_DIR = pathlib.Path(__file__).parent.absolute()

LOCAL_DIR = APP_DIR / "local"
LOCAL_DIR.mkdir(exist_ok=True)


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
    # Add a footer to the main area
    st.markdown(
        '<div style="position: relative; bottom: 0; width: 100%; text-align: center;">'
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
