import io
import os
import shutil
import tempfile

import streamlit as st
from elevenlabs import save
from elevenlabs.client import ElevenLabs

# Preseed ffmpeg env before importing pydub to avoid warnings.
_default_ffmpeg = r"C:\\ProgramData\\chocolatey\\bin\\ffmpeg.exe"
if os.path.exists(_default_ffmpeg):
    os.environ.setdefault("FFMPEG_BINARY", _default_ffmpeg)
    os.environ.setdefault("PATH", os.environ.get("PATH", "") + os.pathsep + os.path.dirname(_default_ffmpeg))

from pydub import AudioSegment

st.set_page_config(page_title="Voice Cloner", page_icon="🎙️", layout="centered")
st.title("🎙️ ElevenLabs Instant Voice Cloner")
st.markdown("Record your voice → Clone instantly → Test your clone!")

# API Key
api_key = st.text_input("ElevenLabs API Key", type="password")
if not api_key:
    st.info("Enter your API key")
    st.stop()

client = ElevenLabs(api_key=api_key)


def configure_ffmpeg():
    """Ensure ffmpeg/ffprobe are available for pydub; raise a clear error if not."""
    env_path = os.getenv("FFMPEG_BINARY")
    candidates = [env_path] if env_path else []
    candidates += [
        "ffmpeg",
        "ffmpeg.exe",
        r"C:\\ProgramData\\chocolatey\\bin\\ffmpeg.exe",  # common Windows install
    ]

    for candidate in candidates:
        if not candidate:
            continue
        resolved = shutil.which(candidate)
        if resolved:
            AudioSegment.converter = resolved
            ffprobe_path = shutil.which("ffprobe")
            if ffprobe_path:
                # Older pydub may not have the attribute; set it defensively.
                if not hasattr(AudioSegment, "ffprobe"):
                    setattr(AudioSegment, "ffprobe", ffprobe_path)
                else:
                    AudioSegment.ffprobe = ffprobe_path
            else:
                # Fallback to converter if ffprobe isn't found; pydub only needs one.
                if not hasattr(AudioSegment, "ffprobe"):
                    setattr(AudioSegment, "ffprobe", resolved)
                else:
                    AudioSegment.ffprobe = resolved
            return resolved

    raise ValueError(
        "ffmpeg is required to decode/encode audio. Install it and ensure it's on PATH, "
        "or set FFMPEG_BINARY to the executable, then restart the app."
    )


# Preconfigure ffmpeg/ffprobe at import time to avoid pydub warnings during first call.
configure_ffmpeg()


def save_audio_to_wav(audio_value):
    """Convert uploaded/recorded audio to a wav file ElevenLabs accepts."""
    configure_ffmpeg()

    raw_bytes = audio_value.getvalue()
    if not raw_bytes:
        raise ValueError("Recording is empty. Please record again.")

    mime = (audio_value.type or "audio/wav").lower()
    input_format = mime.split("/")[-1]
    format_aliases = {
        "mpeg": "mp3",
        "x-wav": "wav",
        "wave": "wav",
        "webm": "webm",
        "ogg": "ogg",
        "opus": "ogg",
        "m4a": "mp4",
    }
    input_format = format_aliases.get(input_format, input_format)

    try:
        audio = AudioSegment.from_file(io.BytesIO(raw_bytes), format=input_format)
    except Exception as exc:  # ffmpeg or decode issue
        raise ValueError(
            "Could not decode the recording. Ensure it's playable audio. "
            "If running locally, install ffmpeg and pydub (pip install pydub)"
        ) from exc

    if audio.duration_seconds < 9.5:
        raise ValueError("Recording too short for cloning (minimum ~10 seconds).")

    # Normalize to a safe mono/44.1kHz wav to satisfy ElevenLabs
    audio = audio.set_channels(1).set_frame_rate(44100)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        audio.export(tmp.name, format="wav", parameters=["-acodec", "pcm_s16le"])

        try:  # quick sanity check the exported wav is readable
            AudioSegment.from_file(tmp.name, format="wav")
        except Exception as exc:
            raise ValueError(
                "Export failed. Ensure ffmpeg is installed and the recording format is supported."
            ) from exc

        return tmp.name, audio.duration_seconds

# Recording
st.header("1. Record Sample (10–60 seconds recommended)")
audio_value = st.audio_input("Click to record")

if audio_value:
    st.audio(audio_value)
    st.success("Recording captured!")
    st.caption(f"Format: {audio_value.type or 'unknown'}")

    if st.button("🔄 Clone This Voice!", type="primary"):
        with st.spinner("Cloning... (10–60 seconds)"):
            sample_path = None
            try:
                sample_path, duration = save_audio_to_wav(audio_value)

                # Instant Voice Cloning method
                with open(sample_path, "rb") as f:
                    cloned_voice = client.voices.ivc.create(
                        name="My Browser Clone",
                        description="Cloned from Streamlit app recording",
                        files=[f]  # Must be list of file handles
                    )

                # Response may be AddVoiceIvcResponseModel with voice_id only
                voice_id = getattr(cloned_voice, "voice_id", None) or cloned_voice
                st.success(f"✅ Cloned! Duration: {duration:.1f}s")
                st.code(f"Voice ID: {voice_id}")

                # Test
                test_text = st.text_input(
                    "Test your clone",
                    value="Hello! This is my cloned voice from the browser. How do I sound?"
                )

                if st.button("🗣️ Test Clone"):
                    with st.spinner("Generating..."):
                        test_audio = client.text_to_speech.convert(
                            voice_id=voice_id,
                            text=test_text,
                            model_id="eleven_multilingual_v2",
                            voice_settings={"stability": 0.75, "similarity_boost": 0.9}
                        )
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as out:
                            save(test_audio, out.name)
                            st.audio(out.name)
                        st.balloons()

            except ValueError as e:
                st.warning(str(e))
            except Exception as e:
                st.error(f"Failed: {str(e)}")
                st.info("""
Common issues:
- Recording too short (<10 seconds) or noisy → try longer/cleaner
- Recording saved as webm/ogg → we try to convert, but ensure ffmpeg is installed
- Free plan quota reached → check https://elevenlabs.io/app/subscription
- Upgrade plan for more clones
- Ensure you have consent to clone the voice
                """)
            finally:
                if sample_path and os.path.exists(sample_path):
                    os.remove(sample_path)

st.markdown("---")
st.subheader("Tips for Great Clones")
st.markdown("""
- Speak naturally with emotion/variation
- Quiet room, no background noise/music
- 30–60 seconds = best quality
- Clone appears in your dashboard → Personal tab
- Copy Voice ID → use in Gemini bot for replies in **your voice**!
""")