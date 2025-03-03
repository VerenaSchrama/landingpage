from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Define FastAPI app
app = FastAPI()

# Define input model for the request body
class QuizInput(BaseModel):
    trimester: str
    dietaryRestrictions: str
    nutritionGoals: str

@app.post("/getRecommendations")
async def get_recommendations(data: QuizInput):
    """Generate pregnancy-friendly food recommendations based on user input."""

    # Define the AI prompt
    prompt = f"""
    A pregnant woman in trimester {data.trimester} follows a {data.dietaryRestrictions} diet and aims for {data.nutritionGoals}.
    Suggest 3 nutritious food items (pulses & grains) that fit her needs. Explain why each food is beneficial and provide a sample product link.
    
    Format response as JSON:
    [
        {{"food": "Food Name", "reason": "Health benefit", "link": "Product URL"}}
    ]
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=300,
            temperature=0.7,
        )

        # Extract the AI-generated response and return it as JSON
        output = response.choices[0].message.content.strip()
        return {"recommendations": output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")