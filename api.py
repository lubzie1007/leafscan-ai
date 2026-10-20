import os
from dotenv import load_dotenv

load_dotenv(override=True)

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import uvicorn
import time
from google import genai
from google.genai import types

from src.ensemble_predict import predict
from src.llm_advisor import get_advice

app = FastAPI(title="Crop Doctor AI API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEBUG_DIR = "debug_uploads"
os.makedirs(DEBUG_DIR, exist_ok=True)

api_key = os.getenv("GEMINI_API_KEY", "").strip()
client = genai.Client(api_key=api_key)

class HealthResponse(BaseModel):
    status: str
    service: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    disease: str
    messages: List[ChatMessage]

@app.get("/", response_model=HealthResponse)
def root():
    return {"status": "ok", "service": "Crop Doctor AI"}

@app.get("/health", response_model=HealthResponse)
def health():
    return {"status": "healthy", "service": "Crop Doctor AI"}

@app.post("/predict")
async def predict_endpoint(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        image_bytes = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read image: {e}")

    debug_path = os.path.join(DEBUG_DIR, f"upload_{int(time.time())}.jpg")
    with open(debug_path, "wb") as f:
        f.write(image_bytes)

    try:
        vision_result = predict(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vision model error: {e}")

    print(f"🔍 Classified as: {vision_result['disease']}")

    try:
        advice = get_advice(vision_result["disease"])
    except Exception as e:
        advice = {"symptoms": "Advice failed.", "treatment": "", "prevention": ""}

    return JSONResponse({
        "disease": vision_result["disease"],
        "confidence": vision_result["confidence"],
        "model_breakdown": {
            "resnet50": {"prediction": vision_result["resnet_prediction"], "confidence": vision_result["resnet_confidence"]},
            "densenet121": {"prediction": vision_result["densenet_prediction"], "confidence": vision_result["densenet_confidence"]},
        },
        "top5": [{"disease": name, "confidence": prob} for name, prob in vision_result["top5"]],
        "symptoms": advice.get("symptoms", ""),
        "treatment": advice.get("treatment", ""),
        "prevention": advice.get("prevention", ""),
    })

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    if not client:
        raise HTTPException(status_code=500, detail="Gemini API key is not configured.")
    try:
        conversation_text = f"Context: {req.disease}\n\n"
        for msg in req.messages:
            role = "Farmer" if msg.role == "user" else "Doctor"
            conversation_text += f"{role}: {msg.content}\n"
        
        conversation_text += "Doctor:"
        
        response = client.models.generate_content(
            model="gemini-3.6-flash", # FORCED 3.5-FLASH
            contents=conversation_text,
            config=types.GenerateContentConfig(
                system_instruction="You are Crop Doctor AI. Answer the farmer's last question concisely and helpfully. Do not use markdown."
            )
        )
        return {"reply": response.text}
    except Exception as e:
        print(f"❌ CHAT ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000)