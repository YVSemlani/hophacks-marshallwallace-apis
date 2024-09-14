from flask import Flask, request, jsonify
import requests
import json
from fuzzywuzzy import process  # Import fuzzywuzzy for fuzzy matching

app = Flask(__name__)

# Define a function to perform fuzzy matching
def fuzzy_match(keyword, datasets):
    descriptions = [dataset['description'] for dataset in datasets]
    # Get the top 5 fuzzy matches for the keyword based on descriptions
    fuzzy_matches = process.extract(keyword, descriptions, limit=5)
    
    # Return the datasets that correspond to the fuzzy matched descriptions
    matching_datasets = [dataset for dataset in datasets if dataset['description'] in [match[0] for match in fuzzy_matches]]
    
    return matching_datasets

@app.route('/search_datasets', methods=['GET'])
def search_datasets():
    keyword = request.args.get('keyword')  # Get the keyword from the URL parameters
    
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    try:
        # Step 1: Get the latest release info with all datasets
        latest_release = requests.get("https://api.semanticscholar.org/datasets/v1/release/latest").json()
        all_datasets = latest_release['datasets']
        
        # Step 2: Perform exact match first
        matching_datasets = [
            dataset for dataset in all_datasets
            if keyword.lower() in dataset['name'].lower() or keyword.lower() in dataset['description'].lower()
        ]
        
        # Step 3: If no exact matches, fall back to fuzzy matching
        if not matching_datasets:
            matching_datasets = fuzzy_match(keyword, all_datasets)

        # Step 4: Return matching datasets as a JSON response
        if matching_datasets:
            return jsonify({
                "keyword": keyword,
                "count": len(matching_datasets),
                "datasets": matching_datasets
            })
        else:
            return jsonify({"message": f"No datasets found matching '{keyword}', even with fuzzy matching."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
