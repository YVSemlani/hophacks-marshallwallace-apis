from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/search_datasets', methods=['GET'])
def search_datasets():
    # Get the keyword from the request URL parameters
    keyword = request.args.get('keyword')
    
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    try:
        # Run the Kaggle API to search for datasets with the given keyword
        print(f"Searching for datasets with keyword: {keyword}")
        result = subprocess.run(['/opt/anaconda3/bin/kaggle', 'datasets', 'list', '-s', keyword], capture_output=True, text=True)
        
        # Parse the response
        datasets = result.stdout.splitlines()[1:]  # Skip the header
        if not datasets:
            return jsonify({"message": f"No datasets found for keyword: {keyword}"}), 404
        
        # Format the datasets into a structured JSON response
        dataset_list = []
        for dataset in datasets:
            columns = dataset.split()
            title = ' '.join(columns[0:2])  # First 2 columns as title
            url = f"https://www.kaggle.com/{columns[0]}"  # URL using the first column
            dataset_list.append({
                "title": title,
                "url": url
            })

        return jsonify({
            "keyword": keyword,
            "count": len(dataset_list),
            "datasets": dataset_list
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
