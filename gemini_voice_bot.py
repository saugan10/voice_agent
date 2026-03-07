import streamlit as st
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import os
import tempfile

# Page setup
st.set_page_config(page_title="Gemini AI Voice Bot", page_icon="🤖", layout="centered")
st.title("🤖 Gemini AI Voice Chat Bot")
st.markdown("Type a message — Gemini thinks & replies with **smart text + natural voice**!")

# Sidebar: API Keys
gemini_api_key = st.sidebar.text_input("Gemini API Key", type="password", help="From https://aistudio.google.com/app/apikey")
elevenlabs_api_key = st.sidebar.text_input("ElevenLabs API Key", type="password")

if not gemini_api_key or not elevenlabs_api_key:
    st.info("👈 Enter both API keys in the sidebar to start")
    st.stop()

# Configure APIs
genai.configure(api_key=gemini_api_key)
eleven_client = ElevenLabs(api_key=elevenlabs_api_key)

# Gemini model (use latest stable/fast)
model = genai.GenerativeModel("gemini-2.5-flash")  # Or "gemini-1.5-pro" for deeper thinking

# Load ElevenLabs voices
@st.cache_data(ttl=600)
def load_voices():
    try:
        response = eleven_client.voices.get_all()
        voices_list = response.voices if hasattr(response, 'voices') and response.voices else []
        return voices_list
    except Exception as e:
        st.error(f"ElevenLabs error: {e}")
        return []

voices = load_voices()
if not voices:
    st.stop()

voice_options = {getattr(v, 'name', 'Unknown'): getattr(v, 'voice_id', None) for v in voices if getattr(v, 'voice_id', None)}
selected_voice_name = st.sidebar.selectbox("Voice for Replies", options=list(voice_options.keys()))
selected_voice_id = voice_options[selected_voice_name]

# Optional: override with a specific cloned voice ID (e.g. from Voice Cloner app)
manual_voice_id = st.sidebar.text_input(
    "Override Voice ID (optional)",
    value="5Bqtc9uVwdleDDqv7cwd",
    help="Paste a specific ElevenLabs voice ID; leave blank to use the selected voice above.",
)
effective_voice_id = manual_voice_id.strip() or selected_voice_id
st.sidebar.caption(f"Using Voice ID: {effective_voice_id}")

# Your 5 styles via voice_settings (NO hidden prompts = zero leakage!)
style_settings = {
    "🔊 Default Voice": {
        "stability": 0.5,
        "similarity_boost": 0.8,
        "style": 0.2,
        "speed": 1.0   # Normal pace
    },
    "🐢 Slow & Clear": {
        "stability": 0.9,    # Very high = super consistent & clear
        "similarity_boost": 0.95,
        "style": 0.0,
        "speed": 0.75        # Obviously slower — big difference!
    },
    "👩‍🏫 Friendly Teacher": {
        "stability": 0.65,   # Balanced for warmth
        "similarity_boost": 0.85,
        "style": 0.5,        # Boosts friendly personality
        "speed": 0.95
    },
    "😌 Calm Reader": {
        "stability": 0.8,    # High for soothing monotone
        "similarity_boost": 0.9,
        "style": 0.1,
        "speed": 0.85        # Relaxed, slightly slower pace
    },
    "⚡ Energetic Guide": {
        "stability": 0.3,    # Low = highly expressive & varied
        "similarity_boost": 0.7,
        "style": 0.8,        # Max exaggeration for excitement
        "speed": 1.2         # Fast & hyped — huge contrast!
    },
}
st.sidebar.header("Speaking Style")
selected_style = st.sidebar.radio("How should replies sound?", options=list(style_settings.keys()))
current_settings = style_settings[selected_style]
st.sidebar.caption({
    "🔊 Default Voice": "Natural neutral",
    "🐢 Slow & Clear": "Extra slow and clear",
    "👩‍🏫 Friendly Teacher": "Warm and encouraging",
    "😌 Calm Reader": "Soothing and relaxed",
    "⚡ Energetic Guide": "Upbeat and exciting"
}[selected_style])

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Optional greeting
    st.session_state.messages.append({"role": "assistant", "content": "Hi! I'm your Gemini-powered voice assistant. Ask me anything!"})

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "audio_path" in msg and os.path.exists(msg["audio_path"]):
            st.audio(msg["audio_path"])

# User input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Gemini response
    with st.chat_message("assistant"):
        with st.spinner("Gemini is thinking..."):
            try:
                # Build chat history for Gemini
                history = []
                for m in st.session_state.messages[:-1]:  # Exclude current user message
                    history.append({"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]})

                chat = model.start_chat(history=history)
                response = chat.send_message(prompt)
                gemini_reply = response.text

                st.markdown(gemini_reply)

                # Generate voice with ElevenLabs
                with st.spinner("Speaking..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                        audio_path = tmp.name

                    audio = eleven_client.text_to_speech.convert(
                        voice_id=effective_voice_id,
                        text=gemini_reply,  # Only the clean Gemini text
                        model_id="eleven_multilingual_v2",
                        voice_settings=current_settings
                    )
                    save(audio, audio_path)
                    st.audio(audio_path)

                # Save to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": gemini_reply,
                    "audio_path": audio_path
                })

            except Exception as e:
                st.error(f"Error: {e}")

# Cleanup old audio files
if len(st.session_state.messages) > 30:
    old = st.session_state.messages[:-15]
    for msg in old:
        if "audio_path" in msg and os.path.exists(msg["audio_path"]):
            os.remove(msg["audio_path"])
    st.session_state.messages = st.session_state.messages[-15:]