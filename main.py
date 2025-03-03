from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError("❌ ERROR: Missing MISTRAL_API_KEY! Set it in the .env file or Render's environment variables.")

# Mistral API settings
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

# Initialize FastAPI
app = FastAPI()

# Define input model
class QuizInput(BaseModel):
    trimester: str
    dietaryRestrictions: str
    nutritionGoals: str

@app.post("/getRecommendations")
async def get_recommendations(data: QuizInput):
    """Fetch AI-generated food recommendations for pregnancy nutrition."""

    prompt = f"""
    A pregnant woman in trimester {data.trimester} follows a {data.dietaryRestrictions} diet and aims for {data.nutritionGoals}.
    Suggest 3 nutritious food items (pulses & grains) that fit her needs. Explain why each food is beneficial.
    Return results in structured JSON format:
    [
        {{"food": "Food Name", "reason": "Health benefit"}}
    ]
    """

    request_data = {
        "model": "mistral-medium",  # Change to "mixtral-8x7b" for better responses
        "messages": [{"role": "system", "content": prompt}],
        "max_tokens": 300,
        "temperature": 0.7
    }

    try:
        response = requests.post(MISTRAL_URL, json=request_data, headers=HEADERS)
        response_data = response.json()

        # Debugging - Log the API response
        print("📌 Mistral API Response:", response_data)

        if "error" in response_data:
            raise HTTPException(status_code=500, detail=f"Mistral API Error: {response_data['error']}")

        return {"recommendations": response_data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()}

    except Exception as e:
        print("❌ Mistral API Request Failed:", e)
        raise HTTPException(status_code=500, detail=f"Request Failed: {str(e)}")
