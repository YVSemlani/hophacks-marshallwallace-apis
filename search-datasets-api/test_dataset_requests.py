import requests
import json

# Update the API URL to match your running Flask server endpoint
API_URL = "http://127.0.0.1:5000/search_datasets"

def test_kaggle_datasets_api(search_term):
    # Pass the keyword as a parameter in the GET request
    params = {"keyword": search_term}
    
    try:
        # Make the GET request to the Flask API
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        
        print(f"Search term: {search_term}")
        print(f"Status code: {response.status_code}")
        
        datasets = response.json()
        print(f"Number of datasets fetched: {datasets.get('count', 0)}")
        
        print(json.dumps(datasets, indent=2))  # Pretty print the response
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    
    print("-" * 50)

# Test cases with different search terms
test_cases = [
    "neuroscience",
    "machine learning",
    "eeg",
    "brain mri",
    "natural language processing"
]

# Run tests for each search term
for case in test_cases:
    test_kaggle_datasets_api(case)

# Test error case (empty search term)
test_kaggle_datasets_api("")
