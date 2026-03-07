from elevenlabs.client import ElevenLabs
import os

# Get API key from environment variable or replace with your key
API_KEY = os.getenv("ELEVENLABS_API_KEY", "your-api-key-here")

client = ElevenLabs(api_key=API_KEY)
voices = client.voices.get_all()

print("Number of voices:", len(voices.voices) if voices else 0)
if voices and voices.voices:
    for v in voices.voices[:5]:  # Print first 5
        print(v.voice_id, v.name)
else:
    print("Empty voices list - key likely invalid")