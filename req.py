import requests

url = "http://localhost:8000/getRecommendations"
data = {
    "trimester": "2",
    "dietaryRestrictions": "vegan",
    "nutritionGoals": "high iron"
}

response = requests.post(url, json=data)
print(response.json())  # Prints AI-generated food recommendations
