import requests
import json

def test_citation_graph(base_url, arxiv_id):
    url = f"{base_url}/citation_graph"
    params = {"arxiv_id": arxiv_id}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        result = response.json()
        print(f"Citation graph for arXiv ID: {arxiv_id}")
        print(json.dumps(result, indent=2))
        
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    base_url = "http://127.0.0.1:2022"  # Adjust if your API is running on a different port
    
    # Test with a valid arXiv ID
    valid_arxiv_id = "1706.03762"  # Transformer paper
    citation_graph = test_citation_graph(base_url, valid_arxiv_id)
    print(json.dumps(citation_graph, indent=2))
    print('-'*50)
    # Test with an invalid arXiv ID
    invalid_arxiv_id = "0000.0000"
    citation_graph = test_citation_graph(base_url, invalid_arxiv_id)
    print(citation_graph)  
    print('-'*50)