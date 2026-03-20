# 🗂️ Project Structure Documentation

## Overview

This document describes the reorganized structure of the Voice Agent project. All files have been organized into logical directories for better maintainability and clarity.

---

## Directory Structure

```
voice_agent/
│
├── 📱 apps/                           # Main Applications
│   ├── elevenlabs_tts_app.py         # Text-to-Speech Streamlit app
│   ├── gemini_voice_bot.py           # AI Voice Chat Bot with Gemini + ElevenLabs
│   ├── voice_cloner_app.py           # Voice Cloning tool
│   ├── gemini_mem0.py                # Advanced voice bot with Mem0 memory
│   └── __init__.py                   # Package initialization
│
├── 🔧 api/                            # API Implementations
│   ├── api.py                        # FastAPI implementation (Easy Read API)
│   ├── api.txt                       # OpenAPI specification
│   └── __init__.py                   # Package initialization
│
├── 🧪 tests/                          # Test Files
│   ├── test_voices.py                # ElevenLabs voice testing utility
│   └── __init__.py                   # Package initialization
│
├── 🛠️ utils/                          # Utility Modules
│   └── __init__.py                   # Package initialization (extensible)
│
├── 📄 requirements.txt                # Python dependencies
├── 📖 README.md                       # Main documentation (comprehensive)
├── 🔒 .env.example                    # Environment variables template
├── 🚫 .gitignore                      # Git ignore rules
└── 📋 PROJECT_STRUCTURE.md            # This file
```

---

## File Details

### 📱 apps/ - Main Applications

All user-facing applications are located here. Each file is a standalone Streamlit application or script that can be run independently.

#### `elevenlabs_tts_app.py`
- **Purpose:** Text-to-Speech interface with 5 voice modulations
- **Run:** `streamlit run apps/elevenlabs_tts_app.py`
- **Dependencies:** ElevenLabs API key
- **Features:**
  - Multiple voice selection
  - 5 speaking styles (Default, Slow & Clear, Friendly Teacher, Calm Reader, Energetic Guide)
  - Emotion tag support
  - MP3 download

#### `gemini_voice_bot.py`
- **Purpose:** AI-powered voice chatbot
- **Run:** `streamlit run apps/gemini_voice_bot.py`
- **Dependencies:** Google Gemini API key, ElevenLabs API key
- **Features:**
  - Natural language understanding via Gemini 2.5 Flash
  - Voice response generation
  - Conversation history
  - Custom voice ID support
  - 5 speaking styles

#### `voice_cloner_app.py`
- **Purpose:** Instant voice cloning tool
- **Run:** `streamlit run apps/voice_cloner_app.py`
- **Dependencies:** ElevenLabs API key, FFmpeg
- **Features:**
  - Browser-based audio recording
  - Automatic format conversion
  - Voice testing
  - Voice ID generation for reuse

#### `gemini_mem0.py`
- **Purpose:** Production-ready voice bot with persistent memory
- **Run:** `python apps/gemini_mem0.py --transport webrtc`
- **Dependencies:** Google Gemini, Deepgram, Cartesia, Mem0 (optional)
- **Features:**
  - Real-time voice conversations
  - Smart turn detection
  - Voice Activity Detection (VAD)
  - Persistent memory across sessions
  - Multiple transport protocols (WebRTC, Daily, Twilio)

---

### 🔧 api/ - API Implementations

API-related code and specifications.

#### `api.py`
- **Purpose:** FastAPI implementation for Easy Read API
- **Run:** `uvicorn api.api:app --reload`
- **Type:** REST API with complete CRUD operations
- **Documentation:** Auto-generated at `/docs` when running

#### `api.txt`
- **Purpose:** OpenAPI 3.0 specification
- **Format:** YAML/OpenAPI
- **Use:** API contract definition, documentation

---

### 🧪 tests/ - Test Files

Testing utilities and scripts.

#### `test_voices.py`
- **Purpose:** Test ElevenLabs API connectivity and list available voices
- **Run:** `python tests/test_voices.py`
- **Use:** Debugging API issues, exploring available voices

**Extensible:** Add more test files here as the project grows.

---

### 🛠️ utils/ - Utility Modules

Reusable utility functions and helper classes.

**Current Status:** Empty (extensible)

**Suggested Future Additions:**
- `audio_processor.py` - Audio manipulation utilities
- `api_client.py` - Shared API client wrappers
- `config.py` - Configuration management
- `validators.py` - Input validation functions

---

### 📄 Root Configuration Files

#### `requirements.txt`
All Python dependencies for the project:
- streamlit
- elevenlabs
- google-generativeai
- pydub
- fastapi
- pydantic
- python-multipart

#### `README.md`
Comprehensive project documentation including:
- Features overview
- Installation instructions
- Usage examples
- API key setup
- Troubleshooting guide

#### `.env.example`
Template for environment variables:
```bash
ELEVENLABS_API_KEY=your_key
GOOGLE_API_KEY=your_key
DEEPGRAM_API_KEY=your_key
CARTESIA_API_KEY=your_key
MEM0_API_KEY=your_key
```

#### `.gitignore`
Excludes sensitive and generated files:
- API keys (`.env`)
- Python cache (`__pycache__/`)
- Virtual environments (`venv/`)
- Generated audio files (`*.mp3`, `*.wav`)
- IDE settings (`.vscode/`, `.idea/`)

---

## Running Applications

### Streamlit Apps (Quick Start)

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run any Streamlit app
streamlit run apps/<app_name>.py
```

### Pipecat Voice Bot

```bash
# Set environment variables
export GOOGLE_API_KEY="your_key"
export DEEPGRAM_API_KEY="your_key"
export CARTESIA_API_KEY="your_key"

# Run with desired transport
python apps/gemini_mem0.py --transport webrtc
```

---

## Development Guidelines

### Adding New Applications

1. Create file in `apps/` directory
2. Follow naming convention: `<feature>_app.py` for Streamlit, `<feature>_bot.py` for scripts
3. Add dependencies to `requirements.txt`
4. Update README.md with new application details
5. Update this file (PROJECT_STRUCTURE.md)

### Adding Utilities

1. Create module in `utils/` directory
2. Use descriptive names: `audio_utils.py`, `api_helpers.py`
3. Add docstrings to all functions
4. Import in other files: `from utils.audio_utils import function_name`

### Adding Tests

1. Create test file in `tests/` directory
2. Use naming convention: `test_<feature>.py`
3. Can use pytest or unittest framework
4. Run tests with: `pytest tests/` or `python -m unittest discover tests/`

---

## File Organization Best Practices

✅ **Do:**
- Keep applications in `apps/`
- Keep test files in `tests/`
- Keep reusable code in `utils/`
- Use descriptive file names
- Add `__init__.py` to make directories packages

❌ **Don't:**
- Mix application code with utility code
- Put test files in root directory
- Commit API keys or `.env` files
- Leave unused files in the project

---

## Migration Notes

### Changes Made (March 2026)

**Before:**
```
voice_agent/
├── elevenlabs_tts_app.py
├── gemini_voice_bot.py
├── voice_cloner_app.py
├── gemini_mem0.py
├── test_voices.py
├── api.py
├── api.txt
├── requirements.txt
└── README.md
```

**After:**
```
voice_agent/
├── apps/
│   ├── elevenlabs_tts_app.py
│   ├── gemini_voice_bot.py
│   ├── voice_cloner_app.py
│   └── gemini_mem0.py
├── api/
│   ├── api.py
│   └── api.txt
├── tests/
│   └── test_voices.py
├── utils/
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

**Benefits:**
- ✅ Clear separation of concerns
- ✅ Easier to navigate and maintain
- ✅ Professional project structure
- ✅ Scalable for future growth
- ✅ Follows Python packaging best practices

---

## Quick Reference

| Task | Command |
|------|---------|
| Run TTS app | `streamlit run apps/elevenlabs_tts_app.py` |
| Run chat bot | `streamlit run apps/gemini_voice_bot.py` |
| Run voice cloner | `streamlit run apps/voice_cloner_app.py` |
| Run advanced bot | `python apps/gemini_mem0.py` |
| Test voices | `python tests/test_voices.py` |
| Run API | `uvicorn api.api:app --reload` |
| Install dependencies | `pip install -r requirements.txt` |

---

**Last Updated:** March 20, 2026
