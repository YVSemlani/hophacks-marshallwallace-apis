from flask import Flask, request, jsonify
from fetch_arxiv_paper_with_citations import fetch_top_citations, fetch_arxiv_paper
import requests

app = Flask(__name__)

@app.route('/citation_graph', methods=['GET'])
def citation_graph():
    arxiv_id = request.args.get('arxiv_id')
    if not arxiv_id:
        return jsonify({"error": "No arXiv ID provided"}), 400
    
    try:
        original_paper = fetch_arxiv_paper(arxiv_id)
        top_citations = fetch_top_citations(arxiv_id, 'arxiv')

        for idx, paper in enumerate(top_citations):
            tertiary_citations = fetch_top_citations(paper['doi'], 'doi')
            top_citations[idx]['top_citations'] = tertiary_citations

        original_paper['top_citations'] = top_citations
    except Exception as e:
        if original_paper is None:
            return jsonify({"error": "Invalid Arxiv ID"}), 500
        return jsonify({"error": str(e)}), 500
    
    return jsonify(original_paper)

if __name__ == '__main__':
    app.run(debug=True)