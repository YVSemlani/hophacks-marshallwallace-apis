import requests
import json

def test_recommend_api(base_url, paper_id, limit=5):
    url = f"{base_url}/recommend"
    params = {
        "paper_id": paper_id,
        "limit": limit
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        print(f"Recommendations for paper ID: {paper_id}")
        print(json.dumps(data, indent=2))
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    base_url = "http://127.0.0.1:5000"  # Adjust if your API is running on a different port
    
    # Test with a valid paper ID
    test_recommend_api(base_url, "42")
    
    # Test with an invalid paper ID
    test_recommend_api(base_url, "invalid_id")
    
    # Test with a different limit
    test_recommend_api(base_url, "42", limit=3)
    
    # Test without a paper ID (should return an error)
    test_recommend_api(base_url, "")