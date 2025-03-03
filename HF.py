from fastapi import FastAPI
import request

app = FastAPI()

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B"
HEADERS = {"Authorization": "Bearer YOUR_HF_API_KEY"}  # Replace with your API key

@app.get("/generate")
def generate(prompt: str):
    payload = {"inputs": prompt}
    response = request.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        return {"response": response.json()[0]["generated_text"]}
    else:
        return {"error": f"{response.status_code} - {response.text}"}
