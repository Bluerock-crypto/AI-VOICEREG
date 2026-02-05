# AI-VOICEREG
# AI-Generated Voice Detection

**Deployed URL:** [https://ai-voicereg-upsidex.onrender.com](https://ai-voicereg-upsidex.onrender.com)  
**API Endpoint:** `https://ai-voicereg-upsidex.onrender.com/api/voice-detection`

## 📖 Project Description
VoxGuard is an AI-powered security tool designed to detect deepfake and AI-generated audio. Built for the **India AI Impact Buildathon**, it analyzes audio artifacts (breathing patterns, background noise, and spectral irregularities) to classify voice samples as **"HUMAN"** or **"AI_GENERATED"**.

The core engine uses **Google Gemini Flash latest **, leveraging its multimodal capabilities to process raw audio data securely and instantly.

---

## 🚀 Features
* **Real-time Analysis:** Returns classification in under 2 seconds.
* **Dual Interface:** * **Web UI:** A user-friendly Neon interface for manual recording and testing.
    * **REST API:** A secure endpoint for programmatic integration.
* **Secure Authentication:** Protected via `x-api-key` headers.
* **Detailed Insights:** Provides a confidence score and a technical explanation for every result.

---

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI, Uvicorn
* **AI Model:** Google Gemini 1.5 Flash (via `google-generativeai`)
* **Frontend:** HTML5, CSS3 (Neon UI), JavaScript (MediaRecorder API)
* **Deployment:** Render (Cloud Hosting)

---

## 🔌 API Documentation (For Judges)

### **Endpoint Details**
* **URL:** `https://ai-voicereg-upsidex.onrender.com/api/voice-detection`
* **Method:** `POST`
* **Auth Header:** `x-api-key`

### **Authentication**
You must include the following header in your request:
```json
{
  "x-api-key": "sk_test_123456789"
}

{
  "language": "Tamil",
  "audioFormat": "mp3",
  "audioBase64": "<BASE64_ENCODED_AUDIO_STRING>"
}

{
  "status": "success",
  "language": "Tamil",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.99,
  "explanation": "The audio lacks natural breathing pauses and exhibits consistent spectral uniformity typical of synthesized speech."
}

📦 ai-voice-detection
 ┣ 📜 index.html        # Frontend User Interface
 ┣ 📜 server.py         # FastAPI Backend & Logic
 ┣ 📜 requirements.txt  # Python Dependencies
 ┗ 📜 README.md         # Documentation
