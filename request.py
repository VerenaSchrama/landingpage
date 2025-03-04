import requests

url = "http://127.0.0.1:8000/getRecommendations"
data = {
    "trimester": "2",
    "dietaryRestrictions": "gluten",
    "nutritionGoals": "more fiber",
    "dislikes": "mushrooms"
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("✅ API Response:", response.json())  # Expected: AI-generated recommendations
else:
    print("❌ Error:", response.status_code, response.text)

