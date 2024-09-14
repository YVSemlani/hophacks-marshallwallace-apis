from flask import Flask, request, jsonify
from fetch_arxiv_paper_with_citations import fetch_top_citations
import networkx as nx
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

def fetch_arxiv_paper(arxiv_id):
    base_url = 'http://export.arxiv.org/api/query?'
    search_query = f'id_list={arxiv_id}'
    full_url = base_url + search_query

    response = requests.get(full_url)
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        entry = root.find('{http://www.w3.org/2005/Atom}entry')
        
        if entry:
            paper = {
                'arxiv_id': arxiv_id,
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
                'authors': [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')],
                'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text.strip(),
                'published': entry.find('{http://www.w3.org/2005/Atom}published').text,
                'link': entry.find('{http://www.w3.org/2005/Atom}id').text
            }
            return paper
    
    return None

def generate_citation_graph(arxiv_id, depth=2):
    G = nx.DiGraph()
    papers_to_process = [(arxiv_id, 0)]
    processed_papers = set()

    while papers_to_process:
        current_id, current_depth = papers_to_process.pop(0)
        if current_id in processed_papers or current_depth > depth:
            continue

        paper = fetch_arxiv_paper(current_id)
        if not paper:
            continue

        G.add_node(current_id, **paper)
        processed_papers.add(current_id)

        top_citations = fetch_top_citations(current_id)
        for citation in top_citations:
            cited_id = citation.get('arxiv_id')
            if cited_id:
                G.add_edge(current_id, cited_id)
                if current_depth < depth:
                    papers_to_process.append((cited_id, current_depth + 1))

    # Connect nodes that share citations
    for node in G.nodes():
        for other_node in G.nodes():
            if node != other_node:
                node_citations = set(G.successors(node))
                other_citations = set(G.successors(other_node))
                shared_citations = node_citations.intersection(other_citations)
                if shared_citations:
                    G.add_edge(node, other_node, shared_citations=len(shared_citations))

    return G

@app.route('/citation_graph', methods=['GET'])
def citation_graph():
    arxiv_id = request.args.get('arxiv_id', default='', type=str)
    if not arxiv_id:
        return jsonify({"error": "No arXiv ID provided"}), 400

    graph = generate_citation_graph(arxiv_id)
    
    # Convert the graph to a dictionary format
    graph_dict = nx.node_link_data(graph)
    
    return jsonify(graph_dict)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)