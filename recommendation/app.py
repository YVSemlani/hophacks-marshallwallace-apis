import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

CORE_API_KEY = "YOUR_CORE_API_KEY_HERE"
CORE_API_URL = "https://api.core.ac.uk/v3/"

def get_recommendations(paper_id, limit=5):
    headers = {
        "Authorization": f"Bearer vCbYHT3eRx58FdjOgAlwkLKWEG4U6QNi"
    }
    params = {
        "limit": limit
    }
    response = requests.get(f"{CORE_API_URL}/v3/recommend/{paper_id}", headers=headers, params=params)

    print(response.json())
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Example URL to test this endpoint:
# http://127.0.0.1:5000/recommend?paper_id=1706.03762&limit=10
# Replace '123456' with a valid paper ID and adjust the limit as needed

if __name__ == '__main__':
    app.run(debug=True)