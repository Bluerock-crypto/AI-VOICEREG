import base64
import json
import os
import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
VALID_API_KEY = "sk_test_123456789"
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

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

# --- THE MISSING ROUTE (HOMEPAGE) ---
@app.get("/")
async def read_root():
    return FileResponse('index.html')

# --- THE API ROUTE ---
@app.post("/api/voice-detection")
async def voice_detection(request: VoiceRequest, x_api_key: str = Header(None)):
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    try:
        encoded = request.audioBase64.split(",", 1)[-1] if "," in request.audioBase64 else request.audioBase64
        audio_bytes = base64.b64decode(encoded)
        
        prompt = f"""
        Analyze this {request.language} audio for AI vs Human traits.
        Return JSON strictly:
        {{
            "classification": "AI_GENERATED" or "HUMAN",
            "confidenceScore": 0.99,
            "explanation": "Technical reason in English AND {request.language}."
        }}
        """
        
        response = model.generate_content([prompt, {"mime_type": "audio/mp3", "data": audio_bytes}])
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        ai_data = json.loads(clean_json)

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
    uvicorn.run(app, host="0.0.0.0", port=10000)
