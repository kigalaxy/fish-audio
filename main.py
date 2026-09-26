import os
from fastapi import FastAPI, Request, Response
import requests

app = FastAPI()

# Holt sich die Keys sicher aus den Umgebungsvariablen von Render
FISH_API_KEY = os.getenv("FISH_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

@app.post("/vapi-tts")
async def handle_vapi_tts(request: Request):
    vapi_data = await request.json()
    text_to_speak = vapi_data.get("text", "")
    sample_rate = vapi_data.get("sampleRate", 24000)

    headers = {
        "Authorization": f"Bearer {FISH_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text_to_speak,
        "voice_id": VOICE_ID,
        "model": "s2.1-pro", # Nutzt das aktuellste Modell
        "format": "pcm",
        "sample_rate": sample_rate
    }

    fish_response = requests.post("https://api.fish.audio/v1/tts", json=payload, headers=headers)
    
    return Response(
        content=fish_response.content, 
        media_type="application/octet-stream"
    )
