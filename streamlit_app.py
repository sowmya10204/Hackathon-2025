# streamlit_app.py
from transformers import pipeline
import streamlit as st
from services.tts_service import text_to_speech_bytes
from utils.text_utils import chunk_text
from transformers import pipeline

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    device=-1  # CPU
)



st.set_page_config(page_title="EchoVerse", layout="wide")
st.title("EchoVerse — AI Audiobook Creator (Open Source Edition)")

with st.sidebar:
    st.header("Settings")
    voice = st.selectbox("Voice", ["Default (gTTS English)"])  # can expand later

    # Language selection
    lang_option = st.selectbox(
        "Select Language",
        ["English", "Hindi", "Spanish", "French", "German", "Japanese"]
    )

# Map language names to gTTS codes
lang_codes = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja"
}

selected_lang = lang_codes[lang_option]


uploaded_file = st.file_uploader("Upload a .txt file (optional)", type=["txt"])
if uploaded_file:
    input_text = uploaded_file.read().decode("utf-8")
else:
    input_text = st.text_area("Paste your text here", height=300)

if st.button("Generate Audio"):
    if not input_text.strip():
        st.warning("Please provide text (paste or upload .txt).")
    else:
        # -------- Emotion Detection --------
        detected_emotion = emotion_classifier(input_text)[0]['label']
        st.info(f"Detected Emotion: {detected_emotion}")

        # -------- Generate Audio --------
        with st.spinner("Generating audio..."):
            chunks = chunk_text(input_text, max_chars=3000)
            full_audio = b""
            for chunk in chunks:
                full_audio += text_to_speech_bytes(chunk, lang=selected_lang)

        st.audio(full_audio, format="audio/mp3")
        st.download_button(
            "Download MP3",
            data=full_audio,
            file_name="echoverse_output.mp3",
            mime="audio/mpeg"
        )
