import arxiv
import json
from datetime import datetime

def fetch_recent_abstracts(categories, search_term, max_results=20):
    all_papers = []
    
    # Create an arXiv Client
    client = arxiv.Client()

    #search_term = search_term.replace(" ", "+")

    # Construct the query with categories and search term in title
    query = f"{search_term}searchtype=all&abstracts=show&order=-announced_date_first&size=100"

    search = arxiv.Search(
        query = search_term,
        max_results = 100,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )

    abstracts = []
    for result in client.results(search):
            published_year = result.published.year  # Extract only the year part
            
            abstracts.append(result.summary)

    return abstracts

def get_recent_papers(search_term):
    categories = ["cs.LG", "cs.AI", "cs.CV", "cs.GT", "cs.CE"]
    papers = fetch_recent_abstracts(categories, search_term)
    return papers

if __name__ == "__main__":
    # This is just for testing the function directly
    search_term = input("Enter a search term for paper titles: ")
    papers = get_recent_papers(search_term)
    print(f"Fetched {len(papers)} recent papers with '{search_term}' in the title")
    if papers:
        print("Most recent paper:")
        print(f"Title: {papers[0]['title']}")
        print(f"Authors: {', '.join(papers[0]['authors'])}")
        print(f"Published: {papers[0]['year']}")
        print(f"arXiv ID: {papers[0]['arxiv_id']}")

