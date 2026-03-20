# 🎙️ Voice Agent - ElevenLabs AI Voice Applications

A collection of powerful voice AI applications built with ElevenLabs and Google Gemini APIs, featuring text-to-speech, voice cloning, and AI-powered voice chat capabilities.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![ElevenLabs](https://img.shields.io/badge/ElevenLabs-Voice%20AI-purple.svg)](https://elevenlabs.io)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini%202.5-green.svg)](https://ai.google.dev/)

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Applications](#-applications)
- [API Keys Setup](#-api-keys-setup)
- [Usage Examples](#-usage-examples)
- [Technologies](#️-technologies-used)
- [Important Notes](#️-important-notes)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Features

This repository contains **four distinct voice AI applications**, each designed for specific use cases:

### 1. 🔊 ElevenLabs Text-to-Speech App
**File:** [`apps/elevenlabs_tts_app.py`](apps/elevenlabs_tts_app.py)

Transform text into natural-sounding speech with multiple voice modulations:
- **Multiple voices** to choose from your ElevenLabs account
- **5 Voice modulations:**
  - 🔊 **Default Voice** - Natural neutral tone
  - 🐢 **Slow & Clear** - Educational, extra slow pace for learning
  - 👩‍🏫 **Friendly Teacher** - Warm and encouraging tone
  - 😌 **Calm Reader** - Soothing, relaxed pace like bedtime stories
  - ⚡ **Energetic Guide** - Upbeat, exciting, and engaging
- Real-time audio generation and playback
- Download generated audio files in MP3 format
- Support for emotion tags (`[laughs]`, `[whispers]`, `[excited]`, etc.)
- Voice preview for all available voices

### 2. 🤖 Gemini AI Voice Chat Bot
**File:** [`apps/gemini_voice_bot.py`](apps/gemini_voice_bot.py)

An intelligent voice chatbot combining Google Gemini AI with ElevenLabs voice synthesis:
- Natural language understanding powered by **Gemini 2.5 Flash**
- Text responses + voice output with adjustable speaking styles
- Customizable voice selection (use any ElevenLabs voice)
- Interactive chat interface with conversation history
- Memory of conversation context across messages
- Five distinct speaking styles controlled via voice settings
- Support for custom voice IDs from Voice Cloner
- Persistent audio files for conversation playback

### 3. 🎙️ Voice Cloner
**File:** [`apps/voice_cloner_app.py`](apps/voice_cloner_app.py)

Clone any voice instantly using ElevenLabs Instant Voice Cloning (IVC):
- Record audio directly in the browser (10-60 seconds recommended)
- Automatic audio format conversion and validation
- Create custom voice clones with descriptions
- Test your cloned voice immediately with custom text
- Supports multiple audio formats (webm, wav, mp3, ogg, m4a, etc.)
- Built-in ffmpeg integration for audio processing
- Voice duration validation (minimum 10 seconds)
- Instant voice cloning in 10-60 seconds

### 4. 🔁 Gemini Mem0 Voice Bot (Advanced)
**File:** [`apps/gemini_mem0.py`](apps/gemini_mem0.py)

Advanced voice bot with persistent memory using the Pipecat framework:
- **Real-time bidirectional voice conversations** via WebRTC/Daily/Twilio
- Powered by Google Gemini LLM
- **Mem0 integration** for long-term memory across sessions
- Deepgram STT (Speech-to-Text)
- Cartesia TTS (Text-to-Speech)
- Smart turn detection (knows when you've finished speaking)
- VAD (Voice Activity Detection) using Silero
- Scalable architecture for production voice applications
- Support for multiple transport protocols

---

## 📁 Project Structure

```
voice_agent/
├── 📱 apps/                           # Main applications
│   ├── elevenlabs_tts_app.py         # Text-to-Speech interface
│   ├── gemini_voice_bot.py           # AI Voice Chat Bot
│   ├── voice_cloner_app.py           # Voice Cloning tool
│   ├── gemini_mem0.py                # Voice Bot with Mem0 memory
│   └── __init__.py
│
├── 🔧 api/                            # API implementations
│   ├── api.py                        # FastAPI implementation (Easy Read)
│   ├── api.txt                       # OpenAPI specification
│   └── __init__.py
│
├── 🧪 tests/                          # Test files
│   ├── test_voices.py                # ElevenLabs voice testing
│   └── __init__.py
│
├── 🛠️ utils/                          # Utility modules (extensible)
│   └── __init__.py
│
├── 📄 requirements.txt                # Python dependencies
├── 📖 README.md                       # This file
├── 🔒 .env.example                    # Environment variables template
└── 🚫 .gitignore                      # Git ignore rules
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** (Python 3.10+ recommended)
- **ElevenLabs API key** → [Get one here](https://elevenlabs.io)
- **Google Gemini API key** → [Get one here](https://aistudio.google.com/app/apikey)
- **FFmpeg** (required for voice cloning and audio processing)
- **Additional APIs** (for `gemini_mem0.py`):
  - Deepgram API key → [deepgram.com/signup](https://deepgram.com/signup)
  - Cartesia API key → [cartesia.ai](https://cartesia.ai)
  - Mem0 API key (optional) → [mem0.ai](https://mem0.ai)

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/saugan10/voice_agent.git
cd voice_agent
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg (Required for Voice Cloning)

#### Windows

**Option 1: Using Chocolatey**
```bash
choco install ffmpeg
```

**Option 2: Using winget**
```bash
winget install ffmpeg
```

**Option 3: Manual Installation**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to system PATH

#### macOS

```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

### 5. Configure Environment Variables (Optional)

For the advanced `gemini_mem0.py` app:

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your API keys
# Use a text editor (notepad, nano, vim, etc.)
```

---

## ⚙️ Configuration

### Option 1: Environment Variables (Recommended for `gemini_mem0.py`)

Create a `.env` file in the root directory:

```bash
# ElevenLabs Configuration
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Google Gemini Configuration
GOOGLE_API_KEY=your_google_gemini_api_key_here

# Deepgram Configuration (for gemini_mem0.py)
DEEPGRAM_API_KEY=your_deepgram_api_key_here

# Cartesia Configuration (for gemini_mem0.py)
CARTESIA_API_KEY=your_cartesia_api_key_here

# Mem0 Configuration (optional, for gemini_mem0.py)
MEM0_API_KEY=your_mem0_api_key_here
```

### Option 2: Enter Keys in App UI (For Streamlit Apps)

All Streamlit applications (`apps/elevenlabs_tts_app.py`, `apps/gemini_voice_bot.py`, `apps/voice_cloner_app.py`) allow you to enter API keys directly in the sidebar interface.

---

## 🎯 Applications

### Running the Applications

Navigate to the project root directory and run:

#### 1. Text-to-Speech App
```bash
streamlit run apps/elevenlabs_tts_app.py
```
Then open: `http://localhost:8501`

#### 2. Gemini Voice Chat Bot
```bash
streamlit run apps/gemini_voice_bot.py
```
Then open: `http://localhost:8501`

#### 3. Voice Cloner
```bash
streamlit run apps/voice_cloner_app.py
```
Then open: `http://localhost:8501`

#### 4. Gemini Mem0 Voice Bot (Pipecat-based)

```bash
# Via WebRTC (default)
python apps/gemini_mem0.py --transport webrtc

# Via Daily.co
python apps/gemini_mem0.py --transport daily --room https://your-daily-room

# Via Twilio
python apps/gemini_mem0.py --transport twilio
```

---

## 🔑 API Keys Setup

### 1. ElevenLabs API Key

1. Sign up at [elevenlabs.io](https://elevenlabs.io)
2. Navigate to your profile settings → **API Keys**
3. Click "Create API Key"
4. Copy your API key
5. Enter it in the application sidebar or add to `.env` file

**Pricing:**
- **Free Tier:** 10,000 characters/month
- **Paid Plans:** Starting at $5/month for 30,000 characters

[View pricing details →](https://elevenlabs.io/pricing)

### 2. Google Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Select a Google Cloud project (or create new)
5. Copy the generated key
6. Enter it in the application sidebar or add to `.env` file

**Free Tier Limits:**
- 15 requests/minute
- 1,500 requests/day
- 1 million tokens/day

[View API documentation →](https://ai.google.dev/docs)

### 3. Additional API Keys (for `gemini_mem0.py`)

#### Deepgram (Speech-to-Text)
- Sign up at [deepgram.com/signup](https://deepgram.com/signup)
- Free tier: $200 credit (45 hours of audio)
- Navigate to API Keys section
- Copy your API key

#### Cartesia (Text-to-Speech)
- Sign up at [cartesia.ai](https://cartesia.ai)
- Navigate to API settings
- Generate and copy API key

#### Mem0 (Optional - Memory Service)
- Sign up at [mem0.ai](https://mem0.ai)
- Create API key in dashboard
- Add to `.env` file

⚠️ **Security Note:** Never commit your API keys to version control. Always use environment variables (`.env` file) or enter them through the application interface.

---

## 📝 Usage Examples

### 1. Text-to-Speech App

**Step-by-step guide:**

1. **Launch the app:**
   ```bash
   streamlit run apps/elevenlabs_tts_app.py
   ```

2. **Enter API key** in the sidebar

3. **Select a voice** from the dropdown menu (preview available)

4. **Choose a speaking style:**
   - 🔊 **Default Voice** - Natural neutral tone
   - 🐢 **Slow & Clear** - Perfect for learning/accessibility
   - 👩‍🏫 **Friendly Teacher** - Warm and encouraging
   - 😌 **Calm Reader** - Soothing bedtime story style
   - ⚡ **Energetic Guide** - Exciting and engaging

5. **Type your text** (supports emotion tags):
   ```
   Hello! [excited] This is amazing! [laughs] 
   Let me whisper [whispers] a secret to you.
   ```

6. Click **"🔊 Generate & Play Audio"**

7. **Download** the generated MP3 file

**Pro Tips:**
- Use emotion tags: `[excited]`, `[sad]`, `[whispers]`, `[laughs]`, `[sighs]`
- Add pauses with ellipsis: `Wait... for it...`
- Emphasize words with CAPS or **asterisks**
- Combine tags with modulations for maximum effect

---

### 2. Gemini Voice Chat Bot

**Step-by-step guide:**

1. **Launch the app:**
   ```bash
   streamlit run apps/gemini_voice_bot.py
   ```

2. **Enter API keys:**
   - Gemini API key
   - ElevenLabs API key

3. **Select a voice** for AI responses

4. **(Optional) Override with custom voice ID** (e.g., from Voice Cloner)

5. **Choose speaking style** for responses

6. **Type your message** in the chat input

7. Gemini generates **intelligent text responses**

8. ElevenLabs converts responses to **natural speech**

**Use Cases:**
- 🎓 Educational tutoring with voice
- 📖 Interactive storytelling for children
- 🌍 Language learning practice
- ♿ Accessibility assistance
- 📞 Customer service simulations
- 🤝 Conversational AI prototyping

**Example Conversations:**

```
User: Tell me a short story about a robot learning to paint.
Gemini: [Generates creative story with emotion and pacing]
        [Story is spoken with selected voice and style]

User: Explain quantum physics in simple terms.
Gemini: [Clear explanation with metaphors]
        [Spoken with Friendly Teacher voice for clarity]
```

---

### 3. Voice Cloner

**Step-by-step guide:**

1. **Launch the app:**
   ```bash
   streamlit run apps/voice_cloner_app.py
   ```

2. **Enter ElevenLabs API key**

3. **Record audio** (click "Click to record"):
   - Speak for **10-60 seconds**
   - Speak naturally with varied emotion
   - Use a **quiet environment** (no background noise)
   - Longer samples (30-60s) produce **better clones**

4. **Preview your recording** to ensure quality

5. Click **"🔄 Clone This Voice!"**

6. Wait **10-60 seconds** for processing

7. **Copy the generated Voice ID:**
   ```
   Voice ID: abc123xyz789
   ```

8. **Test your clone** with custom text

9. **Download audio samples** to verify quality

10. **Use the Voice ID** in other applications:
    - Paste into Gemini Voice Bot "Override Voice ID" field
    - Use in your own ElevenLabs API calls
    - Reference in other projects

**Tips for Best Results:**

✅ **Do:**
- Record in a **quiet room**
- Speak with **natural emotion** and variation
- Include different **tones** (excited, calm, serious)
- Speak for **30-60 seconds** (optimal length)
- Use **clear pronunciation**
- Speak at a **normal pace**

❌ **Don't:**
- Record with background noise or music
- Speak in a monotone voice
- Rush through the recording
- Use recordings shorter than 10 seconds
- Record in echo-y environments
- Use low-quality microphones

---

### 4. Gemini Mem0 Voice Bot (Advanced)

**Production-ready voice bot** using the Pipecat framework.

**Setup:**

```bash
# 1. Set up environment variables
export GOOGLE_API_KEY="your_gemini_key"
export DEEPGRAM_API_KEY="your_deepgram_key"
export CARTESIA_API_KEY="your_cartesia_key"
export MEM0_API_KEY="your_mem0_key"  # Optional

# 2. Choose transport and run
```

**Transport Options:**

**WebRTC (Default):**
```bash
python apps/gemini_mem0.py --transport webrtc
```

**Daily.co (Recommended for production):**
```bash
python apps/gemini_mem0.py --transport daily --room https://your-domain.daily.co/room-name
```

**Twilio:**
```bash
python apps/gemini_mem0.py --transport twilio
```

**Key Features:**
- ✅ Real-time bidirectional voice conversations
- ✅ Smart turn detection (knows when you've finished speaking)
- ✅ Voice Activity Detection (VAD) using Silero
- ✅ Persistent memory across sessions via Mem0
- ✅ Production-ready architecture
- ✅ Multiple transport protocols

**Architecture:**

```
User Voice Input
    ↓
[Deepgram STT] → Speech to Text
    ↓
[Gemini LLM] → Generate Response
    ↓
[Mem0 Memory] → Store/Retrieve Context (optional)
    ↓
[Cartesia TTS] → Text to Speech
    ↓
User Voice Output
```

---

## 🛠️ Technologies Used

### Core Frameworks
- **[Streamlit](https://streamlit.io)** - Interactive web application framework
- **[Pipecat](https://pipecat.ai)** - Real-time voice conversation framework
- **[FastAPI](https://fastapi.tiangolo.com)** - Modern API framework (for api/)

### AI & Voice Services
- **[ElevenLabs](https://elevenlabs.io)** - State-of-the-art voice synthesis and cloning
- **[Google Gemini 2.5 Flash](https://ai.google.dev/)** - Advanced AI language model
- **[Deepgram](https://deepgram.com)** - Speech-to-Text (STT)
- **[Cartesia](https://cartesia.ai)** - High-quality Text-to-Speech (TTS)
- **[Mem0](https://mem0.ai)** - Persistent memory service for AI agents

### Audio Processing
- **[PyDub](https://github.com/jiaaro/pydub)** - Audio manipulation and conversion
- **[FFmpeg](https://ffmpeg.org/)** - Multimedia framework for audio/video processing

### Additional Libraries
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** - Environment variable management
- **[loguru](https://github.com/Delgan/loguru)** - Advanced logging
- **[pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation

---

## ⚠️ Important Notes

### API Costs
- **ElevenLabs:** Charged per character generated (10k free/month)
- **Google Gemini:** Free tier generous (1M tokens/day)
- **Deepgram:** $200 free credit (~45 hours audio)
- **Cartesia & Mem0:** Check respective pricing pages

### Voice Quality
- Higher quality voices may require **premium ElevenLabs plans**
- Professional Voice Cloning requires **paid tier**
- Instant Voice Cloning (IVC) available on **all tiers**

### Audio Requirements
- Voice cloning requires **at least 10 seconds** of clear audio
- Optimal length: **30-60 seconds**
- Background noise significantly impacts quality
- Use high-quality microphones for best results

### Rate Limits
- Be aware of API rate limits based on your plan
- Implement exponential backoff for production apps
- Monitor usage in respective dashboards

### Privacy & Ethics
- ✅ **Always obtain consent** before cloning any voice
- ✅ Respect copyright and intellectual property
- ✅ Use cloned voices responsibly and ethically
- ✅ Comply with ElevenLabs Terms of Service

---

## 🔧 Troubleshooting

### Common Issues

#### 1. FFmpeg Not Found (Voice Cloner)

**Error:** `ffmpeg is required to decode/encode audio`

**Solution:**
```bash
# Windows
choco install ffmpeg
# or
winget install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

After installation, **restart your terminal**.

#### 2. API Key Errors

**Error:** `API key is invalid` or `Unauthorized`

**Solution:**
- Double-check your API key (no extra spaces)
- Ensure key permissions are correct
- Regenerate key if necessary
- Check API dashboard for quota/billing issues

#### 3. Voice Cloning Fails

**Error:** `Recording too short` or `Could not decode`

**Solution:**
- Record for **at least 10 seconds**
- Use a **quiet environment**
- Ensure microphone permissions are granted
- Try a different audio format
- Check ffmpeg installation

#### 4. Streamlit Port Already in Use

**Error:** `Port 8501 is already in use`

**Solution:**
```bash
# Use a different port
streamlit run apps/elevenlabs_tts_app.py --server.port 8502

# Or kill existing Streamlit processes
# Windows
taskkill /F /IM streamlit.exe

# Linux/macOS
pkill -f streamlit
```

#### 5. Import Errors

**Error:** `ModuleNotFoundError: No module named '...'`

**Solution:**
```bash
# Ensure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/amazing-feature`
3. **Commit your changes:** `git commit -m 'Add amazing feature'`
4. **Push to the branch:** `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to functions
- Test your changes thoroughly
- Update README if adding features

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- [ElevenLabs](https://elevenlabs.io) for amazing voice AI technology
- [Google Gemini](https://ai.google.dev/) for powerful language models
- [Streamlit](https://streamlit.io) for the excellent web framework
- [Pipecat](https://pipecat.ai) for real-time voice infrastructure

---

## 📧 Contact & Support

- **GitHub Issues:** [Report bugs or request features](https://github.com/saugan10/voice_agent/issues)
- **Repository:** [github.com/saugan10/voice_agent](https://github.com/saugan10/voice_agent)

---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐️ on GitHub!

---

**Made with ❤️ using ElevenLabs and Google Gemini**

*Last updated: March 2026*
