# 🎙️ Voice Agent - ElevenLabs AI Voice Applications

A collection of powerful voice AI applications built with ElevenLabs and Google Gemini APIs, featuring text-to-speech, voice cloning, and AI-powered voice chat capabilities.

## 🌟 Features

This repository contains three main applications:

### 1. 🔊 ElevenLabs Text-to-Speech App
Transform text into natural-sounding speech with multiple voice modulations:
- **Multiple voices** to choose from
- **5 Voice modulations:**
  - Default Voice (natural)
  - Slow & Clear (educational)
  - Friendly Teacher (warm and encouraging)
  - Calm Reader (soothing and relaxed)
  - Professional Narrator (confident and articulate)
- Real-time audio generation
- Download generated audio files

### 2. 🤖 Gemini AI Voice Chat Bot
An intelligent voice chatbot combining Google Gemini AI with ElevenLabs voice synthesis:
- Natural language understanding powered by Gemini
- Text responses + voice output
- Customizable voice selection
- Interactive chat interface
- Memory of conversation context

### 3. 🎙️ Voice Cloner
Clone any voice instantly using ElevenLabs technology:
- Record audio directly in the browser
- Upload audio files
- Create custom voice clones
- Test your cloned voice immediately
- Manage and delete voice clones

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- ElevenLabs API key ([Get one here](https://elevenlabs.io))
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))
- FFmpeg (for voice cloning)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/saugan10/voice_agent.git
cd voice_agent
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Install FFmpeg (for voice cloning features):
   - **Windows (using Chocolatey):**
     ```bash
     choco install ffmpeg
     ```
   - **macOS:**
     ```bash
     brew install ffmpeg
     ```
   - **Linux:**
     ```bash
     sudo apt-get install ffmpeg
     ```

### Running the Applications

#### Text-to-Speech App
```bash
streamlit run elevenlabs_tts_app.py
```

#### Gemini Voice Chat Bot
```bash
streamlit run gemini_voice_bot.py
```

#### Voice Cloner
```bash
streamlit run voice_cloner_app.py
```

Then open your browser to the URL shown in the terminal (typically `http://localhost:8501`).

## 🔑 API Keys Setup

1. **ElevenLabs API Key:**
   - Sign up at [elevenlabs.io](https://elevenlabs.io)
   - Navigate to your profile settings
   - Copy your API key
   - Enter it in the application sidebar

2. **Google Gemini API Key:**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Copy the key
   - Enter it in the application sidebar (for Gemini Voice Bot)

⚠️ **Important:** Never commit your API keys to version control. Always enter them through the application interface.

## 📁 Project Structure

```
voice_agent/
├── elevenlabs_tts_app.py      # Text-to-speech application
├── gemini_voice_bot.py         # AI voice chatbot
├── voice_cloner_app.py         # Voice cloning application
├── test_voices.py              # Voice testing utility
├── api.py                      # API reference (Easy Read)
├── api.txt                     # OpenAPI specification
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── .gitignore                  # Git ignore rules
```

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io)** - Web application framework
- **[ElevenLabs](https://elevenlabs.io)** - Voice synthesis and cloning
- **[Google Gemini](https://ai.google.dev/)** - AI language model
- **[PyDub](https://github.com/jiaaro/pydub)** - Audio processing
- **[FFmpeg](https://ffmpeg.org/)** - Audio/video processing

## 📝 Usage Examples

### Text-to-Speech
1. Enter your ElevenLabs API key in the sidebar
2. Select a voice from the dropdown
3. Choose a modulation style (e.g., "Friendly Teacher")
4. Type or paste your text
5. Click "Generate Speech" and listen!

### Voice Chat Bot
1. Enter both API keys (Gemini and ElevenLabs)
2. Select a voice for responses
3. Type your message and press Enter
4. Receive AI-generated text and voice responses

### Voice Cloning
1. Enter your ElevenLabs API key
2. Record audio or upload a voice sample
3. Name your voice clone
4. Test generation with sample text
5. Use your cloned voice in other applications!

## ⚠️ Important Notes

- **API Costs:** Both ElevenLabs and Gemini APIs may incur costs based on usage
- **Voice Quality:** Higher quality voices may require premium ElevenLabs plans
- **Audio Length:** Voice cloning requires at least a few seconds of clear audio
- **Rate Limits:** Be aware of API rate limits based on your plan

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [ElevenLabs](https://elevenlabs.io) for amazing voice AI technology
- [Google Gemini](https://ai.google.dev/) for powerful language models
- [Streamlit](https://streamlit.io) for the excellent web framework

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ using ElevenLabs and Google Gemini**
