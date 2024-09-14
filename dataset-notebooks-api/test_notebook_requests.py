import requests
import json

# Update the API URL to match your running Flask server endpoint
API_URL = "http://127.0.0.1:5000/api/notebooks"

def test_kaggle_notebooks_api(dataset_ref):
    # Pass the dataset_ref as a parameter in the GET request
    params = {"dataset_ref": dataset_ref}
    
    try:
        # Make the GET request to the Flask API
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        
        print(f"Dataset reference: {dataset_ref}")
        print(f"Status code: {response.status_code}")
        
        notebooks = response.json()
        if isinstance(notebooks, list):
            print(f"Number of notebooks fetched: {len(notebooks)}")
        else:
            print(f"Response: {notebooks}")
        
        print(json.dumps(notebooks, indent=2))  # Pretty print the response
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    
    print("-" * 50)

# Test cases with different dataset references
test_cases = [
    "uciml/pima-indians-diabetes-database",
    "uciml/red-wine-quality-cortez-et-al-2009",
    "uciml/student-alcohol-consumption",
    ""  # Test with an empty dataset_ref
]

# Run tests for each dataset reference
for case in test_cases:
    test_kaggle_notebooks_api(case)
