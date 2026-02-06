# 🌾 Krishi Sahay — AI Assistant for Farmers

Krishi Sahay is a multilingual, voice-enabled AI assistant built to help Indian farmers get accurate and reliable answers to agriculture-related questions.

The system is designed to answer **only agriculture-specific queries**, such as crops, pests, fertilizers, manure, and soil management, and politely refuse unrelated questions.

---

## 🚜 Problem Statement

Farmers often struggle to access expert agricultural guidance in their own language.  
Existing solutions are either:
- Not multilingual
- Not voice-friendly
- Too technical
- Not focused strictly on agriculture

**Krishi Sahay solves this problem using Generative AI with a farmer-friendly interface.**

---

## ✨ Key Features

- 🌱 Agriculture-only AI responses  
- 🎤 Speech-to-Text (voice queries supported)  
- 🔊 Text-to-Speech (voice answers)  
- 🌍 Multilingual support:
  - English
  - Hindi
  - Telugu
- 🤖 Powered by Groq LLM (LLaMA 3.1)
- 🎨 Clean and intuitive UI built with Streamlit
- 📜 Query history support

---

## 🧠 How It Works

1. User asks a question using text or voice
2. Voice input is converted to text using Whisper
3. Query is processed by a Groq-powered LLM
4. AI generates an agriculture-specific response
5. Answer is displayed and spoken in the selected language

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **LLM:** Groq (LLaMA 3.1)
- **Speech-to-Text:** Faster Whisper
- **Text-to-Speech:** gTTS

---

## ▶️ How to Run the Project

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt