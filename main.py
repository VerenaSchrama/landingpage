import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError("❌ ERROR: Missing MISTRAL_API_KEY! Set it in Render's environment variables.")

# Initialize FastAPI
app = FastAPI(
    title="Pregnancy Nutrition API",
    description="AI-powered food recommendations",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ✅ FIX: Add a root (`/`) route
@app.get("/")
def home():
    return {"message": "FastAPI with Mistral AI is running on Render!"}

# ✅ Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Define input model
class QuizInput(BaseModel):
    trimester: str
    dietaryRestrictions: str
    nutritionGoals: str

@app.get("/")
def home():
    return {"message": "FastAPI is running on Render!"}

# ✅ API endpoint for recommendations
@app.post("/getRecommendations")
async def get_recommendations(data: QuizInput):
    """Fetch AI-generated food recommendations."""
    prompt = f"""
    A pregnant woman in trimester {data.trimester} has dietary restriction: {data.dietaryRestrictions} 
    and nutrition goal: {data.nutritionGoals}. Suggest 3 nutritious food items (pulses & grains).
    Return results in structured JSON:
    {{
        "recommendations": [
            {{"food": "Food Name", "reason": "Health benefit"}},
            {{"food": "Food Name", "reason": "Health benefit"}},
            {{"food": "Food Name", "reason": "Health benefit"}}
        ]
    }}
    """
    payload = {
        "model": "mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post("https://api.mistral.ai/v1/chat/completions", headers={
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

# Ensure correct port for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)