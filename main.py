from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import uuid  # Generate unique IDs

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

# Temporary in-memory storage (for MVP testing)
user_db = {}  # Stores user input: { user_id: user_data }
recommendations_db = {}  # Stores AI-generated responses: { user_id: recommendations }

# Define input model
class UserInput(BaseModel):
    trimester: str
    dietaryRestrictions: str
    nutritionGoals: str
    dislikes: str


# 🔹 1️⃣ POST: Store User Input
@app.post("/userInput", status_code=201)
async def save_user_input(data: UserInput):
    """Store user pregnancy preferences and return a user ID."""
    
    # Generate a unique user ID
    user_id = str(uuid.uuid4())

    # Save input to database
    user_db[user_id] = data.dict()

    # Process AI recommendation immediately
    recommendations_db[user_id] = process_ai_recommendations(user_db[user_id])

    return {"user_id": user_id, "message": "User input stored. Use GET /getRecommendations/{user_id} to retrieve recommendations."}


# 🔹 2️⃣ GET: Retrieve AI-Generated Recommendations
@app.get("/getRecommendations/{user_id}")
async def fetch_recommendations(user_id: str):
    """Retrieve stored recommendations using user ID."""

    if user_id not in recommendations_db:
        raise HTTPException(status_code=404, detail="Recommendations not found. Try submitting user input first.")

    return {"user_id": user_id, "recommendations": recommendations_db[user_id]}


# 🔹 AI Processing Function
def process_ai_recommendations(user_data):
    """Send user input to Mistral AI and return structured recommendations."""
    
    # Create a structured AI prompt
    prompt = f"""
    A pregnant woman in trimester {user_data['trimester']} has the following dietary restriction: {user_data['dietaryRestrictions']} 
    and doesnt eat: {user_data['dislikes']}. She has the following nutrition goals: {user_data['nutritionGoals']}. 
    Suggest 3 nutritious food items (pulses & grains) that fit her needs.
    Explain why each food is beneficial in structured JSON format:
    [
        {{"food": "Food Name", "reason": "Health benefit"}}
    ]
    """

    # Call Mistral AI API
    response = requests.post(
        MISTRAL_URL,
        headers=HEADERS,
        json={"model": "mistral-medium", "messages": [{"role": "user", "content": prompt}]}
    )

    if response.status_code != 200:
        return {"error": "Mistral API Error", "details": response.text}

    return response.json()["choices"][0]["message"]["content"]

# 🔹 Optional: Root Route for API Status
@app.get("/")
def home():
    return {"message": "FastAPI with Mistral AI is running on Render!"}