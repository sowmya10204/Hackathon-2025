# services/tts_service.py
from gtts import gTTS
from io import BytesIO

def text_to_speech_bytes(text: str, lang: str = "en") -> bytes:
    tts = gTTS(text=text, lang=lang)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp.read()
