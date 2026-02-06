import streamlit as st
from groq import Groq
from faster_whisper import WhisperModel
from gtts import gTTS
from dotenv import load_dotenv
import tempfile
import os
import base64
import json
from app import(
    speech_to_text,
    generate_agriculture_answer,
    text_to_speech
)

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Krishi Sahay",
    page_icon="🌾",
    layout="wide"
)

load_dotenv()
# ------------------ SESSION HISTORY ------------------
if "history" not in st.session_state:
    st.session_state.history = []

HISTORY_FILE = "history.json"

if os.path.exists(HISTORY_FILE) and not st.session_state.history:
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        st.session_state.history = json.load(f)

if "query_text" not in st.session_state:
    st.session_state.query_text = ""
# ------------------ LOAD BACKGROUND IMAGE ------------------
def add_bg_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(
                rgba(0,0,0,0.25),
                rgba(0,0,0,0.25)
            ),
            url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: top center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_image("assets/farmer.png")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
.hero {
    text-align: center;
    padding: 2rem 1rem;
    margin-top:-60px;        
}
.title {
    font-size: 3.5rem;
    font-weight: 900;
    color: #1b8f3c;
}
.subtitle {
    font-size: 1.3rem;
    color: #2bbbad;
    margin-top: -0.5rem;
}
.card {
    background-color: #ffffff;
    color: #000000;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.15);
    max-height:300px;
    overflow-y:auto
}
            
.history-card{
    background-color:#f9fff9;
    color: #000000;
    padding: 1rem;
    border-radius:15px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.15);
    max-height:300px;
    overflow-y:auto
    
            }
</style>
""", unsafe_allow_html=True)

# ------------------ MODELS ------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
whisper_model = WhisperModel("small", device="cpu")

# ------------------ FUNCTIONS ------------------
def speech_to_text(audio_path):
    segments, _ = whisper_model.transcribe(audio_path)
    return " ".join([seg.text for seg in segments]).strip()

def generate_answer(query_text, lang):
    prompt = f"""
You are Krishi Sahay, an expert agricultural assistant for Indian farmers.

Rules:
- Answer ONLY agriculture-related questions.
- Topics: crops, pests, fertilizers, manure, soil.
- Politely refuse non-agriculture questions.

Question:
{query_text}

Respond strictly in language code: {lang}.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return temp_audio.name

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.image("assets/logo.png", width=120)
    st.markdown("## 🌾 Krishi Sahay")
    st.markdown("""
**AI-powered agriculture assistant for farmers**

✅ Crops  
✅ Pests & Diseases  
✅ Fertilizers & Manure  
✅ Multilingual (EN / HI / TE)

🚫 Non-agriculture queries are politely declined.
""")

# ------------------ HERO SECTION ------------------
st.markdown("""
<div class="hero">
    <div class="title">KRISHI SAHAY</div>
    <div class="subtitle">Your AI Companion for Smarter Farming 🌱</div>
</div>
""", unsafe_allow_html=True)

# ------------------ LANGUAGE SELECTION ------------------
lang_map = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te"
}

language = st.selectbox("🌍 Choose your language", list(lang_map.keys()))
lang_code = lang_map[language]

# ------------------ INPUT SECTION ------------------
tab1, tab2 = st.tabs(["📝 Text Query", "🎤 Voice Query"])
query_text = ""

with tab1:
    st.session_state.query_text = st.text_area(
        "Ask your agriculture question",
        value=st.session_state.query_text,
        placeholder="Example: Which fertilizer is best for cotton crop?"
    )

with tab2:
    audio_file = st.file_uploader("Upload your voice question (wav/mp3)", type=["wav", "mp3"])
    if audio_file:
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
            temp_audio.write(audio_file.read())
            st.session_state.query_text=speech_to_text(temp_audio.name)
            st.success(f"Recognized Speech: {st.session_state.query_text}")

# ------------------ SUBMIT ------------------
if st.button("🌾 Get Answer"):
    if not st.session_state.query_text.strip():
        st.warning("Please enter or upload a question.")
    else:
        with st.spinner("Krishi Sahay is thinking... 🌱"):
            answer = generate_agriculture_answer(st.session_state.query_text, lang_code)
            st.session_state.history.insert(0, {
                "question": st.session_state.query_text,
                "answer": answer,
                "language": language
            })
            # ------------------ SAVE HISTORY TO FILE ------------------
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
               json.dump(st.session_state.history, f, ensure_ascii=False, indent=2)
        st.markdown("### 🤖 AI Response")
        st.markdown(f"<div class='card'>{answer}</div>", unsafe_allow_html=True)
        
        if st.session_state.history:
            st.markdown("## 📜 Query History")

            for item in st.session_state.history:
              st.markdown(f"""
              <div class="history-card" style="margin-bottom:1rem;">
                <b>🧑‍🌾 Question ({item['language']}):</b><br>
                {item['question']}<br><br>
                <b>🤖 Answer:</b><br>
                {item['answer']}
               </div>
               """, unsafe_allow_html=True)
        st.markdown("<br><br>",unsafe_allow_html=True)
        audio_path = text_to_speech(answer, lang_code)
        st.audio(audio_path, format="audio/mp3")