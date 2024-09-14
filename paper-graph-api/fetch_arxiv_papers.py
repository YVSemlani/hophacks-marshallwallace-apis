import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta

def fetch_arxiv_papers(query, max_results=10):
    base_url = 'http://export.arxiv.org/api/query?'
    
    # Set the search query and parameters
    search_query = f'search_query=all:{query}&start=0&max_results={max_results}'
    
    # Construct the full URL
    full_url = base_url + search_query

    # Send GET request to arXiv API
    response = requests.get(full_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the XML response
        root = ET.fromstring(response.content)
        
        # Extract relevant information from each entry
        papers = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            paper = {
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
                'authors': [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')],
                'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text.strip(),
                'published': entry.find('{http://www.w3.org/2005/Atom}published').text,
                'link': entry.find('{http://www.w3.org/2005/Atom}id').text
            }
            papers.append(paper)
        
        return papers
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return None

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    query = "artificial intelligence"
    papers = fetch_arxiv_papers(query, max_results=20)
    
    if papers:
        # Generate a filename with current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"arxiv_papers_{timestamp}.json"
        
        save_to_json(papers, filename)
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")