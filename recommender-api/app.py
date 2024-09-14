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

@app.route('/recommend', methods=['GET'])
def recommend_papers():
    paper_id = request.args.get('paper_id')
    limit = request.args.get('limit', default=5, type=int)
    
    if not paper_id:
        return jsonify({"error": "Missing paper_id parameter"}), 400
    
    recommendations = get_recommendations(paper_id, limit)
    
    if recommendations:
        return jsonify(recommendations)
    else:
        return jsonify({"error": "Unable to fetch recommendations"}), 500

if __name__ == '__main__':
    app.run(debug=True)