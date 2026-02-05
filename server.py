import base64
import json
import os
import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Buildathon Authentication
VALID_API_KEY = "sk_test_123456789"
SUPPORTED_LANGS = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY")) # Your AIzaSy... key
model = genai.GenerativeModel('models/gemini-2.5-flash')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class VoiceRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

@app.post("/api/voice-detection")
async def voice_detection(request: VoiceRequest, x_api_key: str = Header(None)):
    # Rule 5: API Key Validation
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail={"status": "error", "message": "Invalid API key"})

    try:
        # 1. Clean the Base64 string (removes data:audio/mp3;base64, if present)
        header, encoded = request.audioBase64.split(",", 1) if "," in request.audioBase64 else (None, request.audioBase64)
        audio_bytes = base64.b64decode(encoded)
        
        # 2. Forensic Prompt for Maximum Accuracy
        # Focuses on 'Organic Drift' to prevent misidentifying humans as AI
        prompt = f"""
        Role: Senior Forensic Audio Engineer.
        Target Language: {request.language}
        
        Task: Perform a deep spectral analysis to classify this audio as HUMAN or AI_GENERATED.
        
        ACCURACY PROTOCOL:
        - HUMAN: Look for 'Organic Drift' (unstable pitch), natural breath intakes, dental/labial clicks, and non-linear prosody.
        - AI: Look for 'Robotic Precision' (perfectly stable pitch), lack of breathing, and spectral artifacts in high frequencies.
        
        If the speaker has a natural accent or varies their speed, classify as HUMAN.
        AI is typically too 'clean' and 'rhythmic'.
        
        Return ONLY a JSON object:
        {{
            "classification": "AI_GENERATED" or "HUMAN",
            "confidenceScore": 0.0 to 1.0,
            "explanation": "Brief technical evidence for the classification."
        }}
        """
        
        # 3. Request Analysis
        response = await model.generate_content_async([
            prompt,
            {"mime_type": "audio/mp3", "data": audio_bytes}
        ])
        
        # 4. Parse & Return strictly according to Rule 8 & 9
        ai_data = json.loads(response.text.replace('```json', '').replace('```', '').strip())

        return {
            "status": "success",
            "language": request.language,
            "classification": ai_data["classification"],
            "confidenceScore": float(ai_data["confidenceScore"]),
            "explanation": ai_data["explanation"]
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)