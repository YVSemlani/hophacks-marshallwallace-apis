import requests
import json

def test_hot_or_not_api(base_url, search_term):
    url = f"{base_url}/hot-or-not"
    payload = {
        "search_term": search_term
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"Hot or Not result for search term: '{search_term}'")
        print(json.dumps(result, indent=2))
        
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    base_url = "http://127.0.0.1:5000"  # Adjust if your API is running on a different port
    
    # Test with sample search terms
    search_terms = [
        "Quantum Machine Learning",
        "Renewable Energy",
        "Artificial Intelligence in Healthcare",
        "Blockchain Technology",
        "CRISPR Gene Editing"
    ]
    
    for search_term in search_terms:
        test_hot_or_not_api(base_url, search_term)
        print("-" * 50)