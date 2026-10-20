import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def get_advice(disease_name):
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    
    client = genai.Client(api_key=api_key)
    
    # FORCE 3.5-FLASH AS REQUESTED
    MODEL_NAME = "gemini-3.6-flash"

    SYSTEM_PROMPT = """You are an expert agricultural advisor helping farmers 
    diagnose and treat plant diseases. When given a disease name, respond with 
    a JSON object containing exactly these three fields:

    {
      "symptoms": "A clear description of the visible symptoms (2-4 sentences)",
      "treatment": "Actionable treatment steps, including organic and chemical options (3-5 bullet points as a single string)",
      "prevention": "Preventive measures to avoid recurrence (3-4 bullet points as a single string)"
    }

    Be practical, specific, and use simple language appropriate for farmers.
    Do NOT include any text outside the JSON object."""

    readable = disease_name.replace("___", " - ").replace("_", " ")
    prompt = f"{SYSTEM_PROMPT}\n\nDisease: {readable}"

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        text = response.text.strip()

        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        result = json.loads(text)
        return {
            "symptoms":    result.get("symptoms", ""),
            "treatment":   result.get("treatment", ""),
            "prevention":  result.get("prevention", ""),
        }

    except Exception as e:
        print(f"🚨 LLM ADVISOR ERROR: {e}")
        return {
            "symptoms":    f"Error: {e}",
            "treatment":   "",
            "prevention":  "",
        }
    
if __name__ == "__main__":
    # Quick test
    for disease in [
        "Tomato___Early_blight",
        "Potato___Late_blight",
        "Apple___Apple_scab",
    ]:
        print("=" * 60)
        print(f"Disease: {disease}")
        print("=" * 60)
        advice = get_advice(disease)
        print(f"\n📋 SYMPTOMS:\n{advice['symptoms']}")
        print(f"\n💊 TREATMENT:\n{advice['treatment']}")
        print(f"\n🛡️  PREVENTION:\n{advice['prevention']}")
        print()