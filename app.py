from groq import Groq
from faster_whisper import WhisperModel
from gtts import gTTS
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()

# ------------------ MODELS ------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
whisper_model = WhisperModel("small", device="cpu")

# ------------------ SPEECH TO TEXT ------------------
def speech_to_text(audio_path: str) -> str:
    segments, _ = whisper_model.transcribe(audio_path)
    return " ".join([seg.text for seg in segments]).strip()

# ------------------ TEXT TO SPEECH ------------------
def text_to_speech(text: str, lang: str) -> str:
    tts = gTTS(text=text, lang=lang)
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return temp_audio.name

# ------------------ AGRICULTURE AI ------------------
def generate_agriculture_answer(query_text: str, lang: str) -> str:
    prompt = f"""
You are Krishi Sahay, an expert agricultural assistant for Indian farmers.

Rules:
- ONLY answer questions related to agriculture.
- Topics allowed: crops, pests, diseases, fertilizers, manure, soil.
- If the question is NOT agriculture-related, politely refuse.

Question:
{query_text}

Respond strictly in language code: {lang}.
Give a clear, practical, farmer-friendly answer.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()