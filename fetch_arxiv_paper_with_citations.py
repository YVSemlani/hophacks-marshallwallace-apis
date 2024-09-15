import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime
from flask import Flask, jsonify

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
    
    print(f"Error: Unable to fetch data. Status code: {response.status_code}")
    return None

def fetch_doi_citations(doi):
    semantic_scholar_url = f"https://api.semanticscholar.org/v1/paper/doi:{doi}"
    response = requests.get(semantic_scholar_url)

def fetch_top_citations(some_id, id_type, top_n=5):
    if id_type == 'arxiv':
        semantic_scholar_url = f"https://api.semanticscholar.org/v1/paper/arxiv:{some_id}"
    elif id_type == 'doi':
        semantic_scholar_url = f"https://api.semanticscholar.org/v1/paper/doi:{some_id}"
    else:
        print("Invalid ID type")
        return []
    response = requests.get(semantic_scholar_url)
    
    if response.status_code == 200:
        data = response.json()
        all_citations = data.get('citations', [])
        if all_citations == []:
            all_citations = data.get('references', [])
        
        # Sort citations by citationCount in descending order and take top N
        top_citations = sorted(all_citations, key=lambda x: x.get('citationCount', 0), reverse=True)[:top_n]
        
        if id_type == 'doi':
            print(top_citations)
        # Extract relevant information and arXiv ID if available
        processed_citations = []
        for citation in top_citations:
            print(citation)
            doi = citation['doi']
        
            processed_citations.append({
                'title': citation.get('title'),
                'authors': [author.get('name') for author in citation.get('authors', [])],
                'year': citation.get('year'),
                'citationCount': citation.get('citationCount'),
                'doi': doi
            })
        
        return processed_citations
    
    print(f"Error: Unable to fetch citations. Status code: {response.status_code}")
    return []

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    arxiv_id = "1706.03762"  # Example arXiv ID
    original_paper = fetch_arxiv_paper(arxiv_id)

    print(original_paper)
    print('-'*50)
    
    if original_paper:
        top_citations = fetch_top_citations(arxiv_id, 'arxiv')

        print(type(top_citations))
        print('-'*50)

        for idx, paper in enumerate(top_citations):
            print(paper['doi'])
            tertiary_citations = fetch_top_citations(paper['doi'], 'doi')
            print(tertiary_citations)
            top_citations[idx]['top_citations'] = tertiary_citations

        original_paper['top_citations'] = top_citations

        print(json.dumps(original_paper, indent=4))
        print('-'*50)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"arxiv_paper_with_top_citations_{timestamp}.json"
        
        #save_to_json(paper, filename)
        print(f"Data saved to {filename}")
        print(f"Number of top citations: {len(top_citations)}")
    else:
        print("No data to save.")