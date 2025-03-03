from fastapi import FastAPI, HTTPException
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API Key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Create FastAPI app
app = FastAPI()

# Test API Key by listing available models
@app.get("/check-openai")
async def check_openai():
    try:
        models = client.models.list()
        return {"message": "OpenAI API is working!", "models": [m.id for m in models.data]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")
