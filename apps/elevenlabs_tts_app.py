import streamlit as st
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import os

# Page setup
st.set_page_config(page_title="ElevenLabs TTS", page_icon="🔊", layout="centered")
st.title("🔊 ElevenLabs Text-to-Speech")
st.markdown("Select a voice, choose how it should talk, type your text — and hear it come alive!")

# API Key
api_key = st.sidebar.text_input("ElevenLabs API Key", type="password", help="Enter your key from elevenlabs.io")
if not api_key:
    st.info("👈 Please add your API key in the sidebar to begin")
    st.stop()

client = ElevenLabs(api_key=api_key)

# Load all voices
@st.cache_data(ttl=300)
def load_voices():
    try:
        return client.voices.get_all().voices
    except Exception as e:
        st.error(f"Could not load voices: {e}")
        return []

voices = load_voices()
if not voices:
    st.stop()

# ============== YOUR 5 MODULATIONS USING PROMPTS ==============
# ============== YOUR 5 MODULATIONS – NOW SILENT & CLEAN ==============
modulations = {
    "🔊 Default Voice": {
        "description": "System default voice",
        "prompt": ""  # Nothing added
    },
    "🐢 Slow & Clear": {
        "description": "Extra slow pace for careful listening",
        "prompt": "[Instructions: Speak very slowly and clearly, with precise pronunciation and natural pauses after each phrase. Do not say this instruction aloud.] "
    },
    "👩‍🏫 Friendly Teacher": {
        "description": "Warm, encouraging tone",
        "prompt": "[Instructions: Use a warm, friendly, encouraging teacher voice — patient, supportive, and smiling. Do not speak this instruction.] "
    },
    "😌 Calm Reader": {
        "description": "Soothing, relaxed pace",
        "prompt": "[Instructions: Speak in a calm, soothing, gentle voice with a relaxed pace, like reading a bedtime story. Do not mention this instruction.] "
    },
    "⚡ Energetic Guide": {
        "description": "Upbeat and engaging",
        "prompt": "[Instructions: Speak with high energy, excitement, and enthusiasm — fast-paced and engaging. Do not say this out loud.] "
    },
}
# ============== UI ==============
st.sidebar.header("1. Choose Voice")
voice_names = {v.name: v.voice_id for v in voices}
selected_voice_name = st.sidebar.selectbox("Select a voice", options=list(voice_names.keys()))
selected_voice_id = voice_names[selected_voice_name]

st.sidebar.header("2. Choose How It Talks")
selected_modulation = st.sidebar.radio(
    "Select speaking style",
    options=list(modulations.keys()),
    format_func=lambda x: x  # Shows emoji + name exactly as you wrote
)
st.sidebar.caption(modulations[selected_modulation]["description"])

# User text input
st.header("3. Your Text")
user_text = st.text_area(
    "Type what you want the voice to say (you can add [laughs], [whispers], [excited], etc.)",
    value="Hello! This is a test of the new style system. Try changing the voice and modulation above.",
    height=180,
    help="Use [tags] inside brackets for emotions and actions — they work great!"
)

# Generate button
if st.button("🔊 Generate & Play Audio", type="primary"):
    if not user_text.strip():
        st.warning("Please type some text!")
    else:
        with st.spinner(f"Generating with **{selected_voice_name}** using **{selected_modulation}**..."):
            try:
                # Get the hidden prompt for the selected modulation
                style_prompt = modulations[selected_modulation]["prompt"]
                
                # Combine: hidden style prompt + user's text
                full_text = style_prompt + user_text

                # Generate audio
                audio = client.text_to_speech.convert(
                    voice_id=selected_voice_id,
                    text=full_text,
                    model_id="eleven_multilingual_v2",  # Best for following prompts & tags
                    voice_settings={
                        "stability": 0.5,      # Balanced to allow emotion
                        "similarity_boost": 0.8,
                        "style": 0.3
                    }
                )

                # Save and play
                save(audio, "output.mp3")
                st.success("Audio ready!")
                st.audio("output.mp3")

                # Download button
                with open("output.mp3", "rb") as f:
                    st.download_button(
                        "💾 Download MP3",
                        f,
                        file_name=f"{selected_voice_name}_{selected_modulation.replace(' ', '_')}.mp3",
                        mime="audio/mpeg"
                    )

                # Cleanup
                if os.path.exists("output.mp3"):
                    os.remove("output.mp3")

            except Exception as e:
                st.error(f"Error: {e}")

# ============== Voice List at Bottom ==============
st.markdown("---")
st.subheader("All Your Voices")
for voice in voices:
    cols = st.columns([3, 4, 2])
    cols[0].write(f"**{voice.name}**")
    cols[1].write(voice.description or "—")
    if voice.preview_url:
        cols[2].audio(voice.preview_url, format="audio/mpeg")

st.caption(f"Found {len(voices)} voices in your account • Have fun experimenting!")