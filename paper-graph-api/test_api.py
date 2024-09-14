import requests

API_URL = "http://localhost:3000/recent_papers"

def test_citation_graph_api(arxiv_id):
    params = {"arxiv_id": arxiv_id}
    try:
        response = requests.get(API_URL.replace('recent_papers', 'citation_graph'), params=params)
        response.raise_for_status()
        
        print(f"arXiv ID: {arxiv_id}")
        print(f"Status code: {response.status_code}")
        
        graph_data = response.json()
        print(f"Number of nodes: {len(graph_data['nodes'])}")
        print(f"Number of edges: {len(graph_data['links'])}")
        
        print("\nFirst few nodes:")
        for node in graph_data['nodes'][:5]:
            print(f"- {node['id']}: {node.get('title', 'N/A')}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    
    print("-" * 50)

# Test citation graph
test_citation_graph_api("1706.03762")  # arXiv ID for "Attention Is All You Need" paper