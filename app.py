from groq import Groq
from faster_whisper import WhisperModel
from dotenv import load_dotenv
from gtts import gTTS
import os

load_dotenv()

print("Starting KrishiSahay — FINAL MODE (Voice → Multilingual Audio)")

# ------------------ MODELS ------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
whisper_model = WhisperModel("small", device="cpu")

# ------------------ SPEECH TO TEXT ------------------
def speech_to_text(audio_path):
    segments, _ = whisper_model.transcribe(audio_path)
    return " ".join([seg.text for seg in segments]).strip()

# ------------------ TEXT TO SPEECH ------------------
def speak_text(text, lang, filename="answer.mp3"):
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

    print(f"[DEBUG] Audio saved as {filename}")
    os.startfile(os.path.abspath(filename))  # guaranteed on Windows

# ------------------ MAIN ------------------
print("\nSelect language for answer:")
print("en - English")
print("hi - Hindi")
print("te - Telugu")

lang = input("Enter language code: ").strip().lower()

if lang not in ["en", "hi", "te"]:
    print("Invalid language, defaulting to English.")
    lang = "en"

audio_path = "audio/question.wav"
print("\nListening to audio:", audio_path)

query_text = speech_to_text(audio_path)
print("Recognized speech:", query_text)

prompt = f"""
You are an expert agricultural assistant for Indian farmers.

The farmer asked:
{query_text}

Respond in this language code: {lang}.
Give a clear, helpful agricultural answer.
"""

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3
)

final_answer = response.choices[0].message.content.strip()

print("\n✅ Final Answer:")
print(final_answer)

print("\n🔊 Playing audio answer...")
speak_text(final_answer, lang)