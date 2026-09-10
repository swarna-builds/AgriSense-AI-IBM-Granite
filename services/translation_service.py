import io
import re
import logging
from gtts import gTTS
import speech_recognition as sr

def _get_lang_metadata(target_lang: str) -> tuple:
    tl = str(target_lang).lower().strip()
    if "kn" in tl or "kannada" in tl:
        return "Kannada", "kn", "kn-IN"
    elif "hi" in tl or "hindi" in tl:
        return "Hindi", "hi", "hi-IN"
    elif "te" in tl or "telugu" in tl:
        return "Telugu", "te", "te-IN"
    elif "ta" in tl or "tamil" in tl:
        return "Tamil", "ta", "ta-IN"
    return "English", "en", "en-IN"

def extract_number_from_text(text: str, default: int = 35) -> int:
    """Extracts spoken or typed integers for crop age slider inputs."""
    if not text:
        return default
    matches = re.findall(r'\b\d+\b', str(text))
    if matches:
        val = int(matches[0])
        return max(5, min(150, val))
    return default

def match_dropdown_voice(transcribed_text: str, valid_keys: list) -> str:
    """Matches spoken text against available dropdown options."""
    if not transcribed_text:
        return None
    tt = str(transcribed_text).lower()
    for key in valid_keys:
        if key.lower() in tt:
            return key
    return None

def transcribe_audio_to_text(audio_file, target_lang: str = "en") -> str:
    """Speech-to-Text: Converts spoken audio buffer into transcribed text."""
    if not audio_file:
        return ""
    
    _, _, locale = _get_lang_metadata(target_lang)
    recognizer = sr.Recognizer()
    
    try:
        audio_bytes = audio_file.read()
        audio_buffer = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_buffer) as source:
            audio_data = recognizer.record(source)
            transcription = recognizer.recognize_google(audio_data, language=locale)
            return transcription.strip()
    except Exception as e:
        logging.warning(f"STT recognition error: {e}")
        return ""

def translate_text(text: str, target_lang: str) -> str:
    """Translates text using IBM watsonx engine or fallback."""
    if not text or not isinstance(text, str):
        return text

    target_name, target_code, _ = _get_lang_metadata(target_lang)
    if target_name == "English":
        return text

    try:
        import streamlit as st
        if "engine" in st.session_state and st.session_state.engine and st.session_state.engine.model:
            system_prompt = f"You are an expert translator. Translate the following agricultural text into natural, fluent {target_name}. Output ONLY the translated text in {target_name} script."
            user_prompt = f"Text to translate:\n{text}"
            
            response = st.session_state.engine.model.generate_text(
                prompt=f"<|system|>\n{system_prompt}\n<|user|>\n{user_prompt}\n<|assistant|>\n"
            )
            if response and response.strip():
                return response.strip()
    except Exception:
        pass

    try:
        from deep_translator import MyMemoryTranslator
        return MyMemoryTranslator(source='en-GB', target=f"{target_code}-IN").translate(text)
    except Exception:
        return text

def generate_audio(text: str, target_lang: str):
    """Text-to-Speech: Generates MP3 stream for spoken audio."""
    if not text or not isinstance(text, str):
        return None

    _, code, _ = _get_lang_metadata(target_lang)
    try:
        tts = gTTS(text=text, lang=code, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception as e:
        logging.warning(f"TTS generation error: {e}")
        return None