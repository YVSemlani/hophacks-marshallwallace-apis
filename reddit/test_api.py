import requests
import json
import time

API_URL = "http://127.0.0.1:5000/analyze_reddit_sentiment"

def test_reddit_sentiment_analysis(search_term):
    payload = {
        "search_term": search_term
    }
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        
        print(f"Search term: {search_term}")
        print(f"Status code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    print("-" * 50)

# Test cases
test_cases = [
    "artificial intelligence",
    "climate change",
    #"space exploration",
    #"cryptocurrency",
    #"renewable energy"
]

# Run tests
for case in test_cases:
    test_reddit_sentiment_analysis(case)