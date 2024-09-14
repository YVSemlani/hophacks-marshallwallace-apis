from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

def fetch_kaggle_notebooks(dataset_ref):
    print(f"Fetching notebooks for dataset_ref: {dataset_ref}")  # Debugging line
    try:
        result = subprocess.run(
            ['kaggle', 'kernels', 'list', '--dataset', dataset_ref],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Subprocess result: {result.stdout}")  # Debugging line
        if result.returncode != 0:
            raise Exception(result.stderr)
        
        # Process the output line by line
        lines = result.stdout.strip().split("\n")
        headers = lines[0].split()  # First line is the header

        # Parse each line into a dictionary based on the header columns
        notebooks = []
        for line in lines[1:]:
            cols = line.split()
            if len(cols) < 5:  # Skip any invalid lines that don't have the expected number of columns
                continue
            
            # Try to parse totalVotes and handle cases where it can't be converted
            try:
                total_votes = int(cols[-1])  # The last column is totalVotes
            except ValueError:
                continue  # Skip rows where totalVotes isn't a valid number
            
            notebook = {
                'ref': cols[0],
                'title': " ".join(cols[1:-3]),  # Title might have spaces
                'author': cols[-3],
                'lastRunTime': cols[-2],
                'totalVotes': total_votes
            }
            notebooks.append(notebook)

        # Sort notebooks by 'totalVotes'
        sorted_notebooks = sorted(notebooks, key=lambda x: x['totalVotes'], reverse=True)
        return sorted_notebooks
    except Exception as e:
        print(f"Error fetching notebooks: {e}")  # Debugging line
        return str(e)

@app.route('/api/notebooks', methods=['GET'])
def get_notebooks():
    dataset_ref = request.args.get('dataset_ref')
    print(f"Received dataset_ref: {dataset_ref}")  # Debugging line

    if not dataset_ref:
        return jsonify({"error": "Please provide a dataset_ref parameter."}), 400

    notebooks = fetch_kaggle_notebooks(dataset_ref)
    print(f"Notebooks fetched: {notebooks}")  # Debugging line
    
    if isinstance(notebooks, str):  # If an error message was returned
        return jsonify({"error": notebooks}), 500

    return jsonify(notebooks)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
