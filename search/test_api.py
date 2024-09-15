import requests
import json

API_URL = "http://localhost:5000/recent_papers"

def test_recent_papers_api(search_term):
    params = {"search_term": search_term}
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        
        print(f"Search term: {search_term}")
        print(f"Status code: {response.status_code}")
        
        papers = response.json()
        print(f"Number of papers fetched: {len(papers)}")
        
        print(papers)
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    
    print("-" * 50)

# Test cases
test_cases = [
    "machine learning",
    "quantum computing",
    "neural networks",
    "computer vision",
    "natural language processing"
]

# Run tests
for case in test_cases:
    test_recent_papers_api(case)

# Test error case (empty search term)
test_recent_papers_api("")