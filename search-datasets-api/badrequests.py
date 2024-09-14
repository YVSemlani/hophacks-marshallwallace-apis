import requests
import json

# Define the API URL
API_URL = "http://127.0.0.1:5000/search_datasets"

def test_datasets_api(keyword):
    params = {"keyword": keyword}  # The parameter is 'keyword'
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Raise an error for bad responses (e.g., 4xx, 5xx)
        
        print(f"Search term: {keyword}")
        print(f"Status code: {response.status_code}")
        
        datasets = response.json()
        if "datasets" in datasets:
            print(f"Number of datasets fetched: {len(datasets['datasets'])}")
            print(json.dumps(datasets, indent=2))  # Print the JSON response in a pretty format
        elif "message" in datasets:
            print(datasets["message"])  # Gracefully handle no datasets found
        else:
            print("Unexpected response format.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    
    print("-" * 50)

# Test cases
test_cases = [
    "neuroscience",
    "bioinformatics",
    "machine learning",
    "deep learning",
    "natural language processing"
]

# Run tests
for case in test_cases:
    test_datasets_api(case)

# Test error case (empty search term)
test_datasets_api("")
