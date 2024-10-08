import time
from flask import jsonify, request
import requests
from config.app import app
from graph.app import generate_citation_graph
from reddit.route import analyze_sentiment as analyze_reddit, fetch_reddit_posts
from search.fetch_recent_arxiv_papers import get_recent_papers
import networkx as nx
from fetch_arxiv_paper_with_citations import fetch_top_citations, fetch_arxiv_paper
#from flask_cors import CORS

#CORS(app)

# Add these constants from the recommender-api
CORE_API_KEY = "vCbYHT3eRx58FdjOgAlwkLKWEG4U6QNi"
CORE_API_URL = "https://api.core.ac.uk/v3/recommend"

OPENROUTER_API_KEY = "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" #os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Add this function from the recommender-api
def get_recommendations(data):
    headers = {
        "Authorization": f"Bearer {CORE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(CORE_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Add this new route from the recommender-api
@app.route('/recommend', methods=['POST'])
def recommend_papers():
    data = request.json
    required_params = ['limit', 'identifier', 'abstract', 'title']
    data['text'] = data['abstract']
    data['result_type'] = 'article'
    
    for param in required_params:
        if param not in data:
            return jsonify({"error": f"Missing required parameter: {param}"}), 400
    
    # Optional parameters
    if 'authors' in data and not isinstance(data['authors'], list):
        return jsonify({"error": "Authors must be an array of strings"}), 400
    
    if 'data_provider_id' in data and not (isinstance(data['data_provider_id'], int) or data['data_provider_id'] is None):
        return jsonify({"error": "data_provider_id must be an integer or null"}), 400
    
    recommendations = get_recommendations(data)
    
    if recommendations:
        return jsonify(recommendations)
    else:
        return jsonify({"error": "Unable to fetch recommendations"}), 500

@app.route("/")
def welcome():
    return "Welcome to Spotinder!"

@app.route('/recent_papers', methods=['GET'])
def recent_papers():
    search_term = request.args.get('search_term', default='', type=str)
    if not search_term:
        return jsonify({"error": "No search term provided"}), 400
    
    papers = get_recent_papers(search_term)
    return jsonify(papers)

@app.route('/analyze_reddit_sentiment', methods=['GET'])
def analyze_reddit_sentiment():
    search_term = request.args.get('search_term', default='', type=str)
    
    if not search_term:
        return jsonify({"error": "No search term provided"}), 400

    posts = fetch_reddit_posts(search_term)
    
    sentiments = []
    for post in posts:
        while True:
            try:
                print("Analyzing sentiment for post: ", post)
                sentiment = analyze_reddit(post, search_term)
                if sentiment is not None:
                    sentiments.append(sentiment)
                break
            except requests.exceptions.HTTPError as e:
                print("Error: ", e)
                if e.response.status_code == 429:
                    time.sleep(11)  # Wait for 5 seconds before retrying
                else:
                    raise

    if sentiments:
        average_sentiment = sum(sentiments) / len(sentiments)
    else:
        average_sentiment = 0

    return jsonify({
        "search_term": search_term,
        "average_sentiment": average_sentiment,
        "num_posts_analyzed": len(sentiments)
    })

@app.route('/analyze_sentiment', methods=['GET'])
def analyze_sentiment():
    OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
    OPENROUTER_API_KEY = "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" #os.environ.get("OPENROUTER_API_KEY")
    model = "openai/gpt-4o-mini-2024-07-18" #"nousresearch/hermes-3-llama-3.1-405b:free"

    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")
    
    text = request.args.get('text', default='')
    search_term = request.args.get('search_term', default='', type=str)

    if not text:
        return jsonify({
            "error": "No text provided",
            "token_count": 0
        }), 400

    
    # Prepare the prompt for sentiment analysis
    prompt = f'''I will provide you a research abstract and a search term. 
    The only output you will provide is a sentiment score between -1 and 1 from most negative to most positive. 
    This sentiment score should be with relation to the search term. 
    Respond with only a sentiment score between -1 and 1. Your output should never be non-numeric.

    Your overarching goal is to help researchers get an idea for the general sentiment of the community towards an a particular topic.
    Abstract: {text} 
    Search Term: {search_term}'''
    

    # Prepare the request to OpenRouter
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "seed": 42
    }

    try:
        response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        sentiment_text = result['choices'][0]['message']['content'].strip().lower()
        try:
            sentiment = float(sentiment_text)
        except ValueError:
            # If parsing fails, set sentiment to None or a default value
            sentiment = None
    
        return jsonify({
            "sentiment": sentiment,
            "token_count": len(text.split())  # Simple word count as a proxy for tokens
        })

    except requests.exceptions.RequestException as e:
        print(str(e))
        return jsonify({
            "error": str(e),
            "token_count": len(text.split())
        }), 500


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

def create_json(search_term):
    abstracts = get_recent_papers(search_term)
    json = {
        "abstracts": abstracts,
        "search_term": search_term
    }
    return json

@app.route('/hot-or-not', methods=['GET', 'OPTIONS'])
def hot_or_not():
    search_term = request.args.get('search_term')
    if not search_term:
        print(request.args)
        return jsonify({"error": "No search term provided"}), 400

    text = create_json(search_term)
    prompt = f'''I am providing you with a set of abstracts for research papers. I am also providing you with a search term.
    Your goal is to determine, given the content of the abstracts, whether the research topic indicated by the search term is currently 'hot' and forecast its future.
    You should use the content of the abstracts, prior knowledge of the topic, your knowledge of the search term, and any statistics on the papers to determine the current state of the field and its future.
    Explain your reasoning in  a brief paragraph that ends with a recommendation of whether the field is 'hot' or 'not' using the fire emoji or the frozen fire emoji. 
    
    The format of the output should be text in this:

    [
        "reasoning": "<brief paragraph explaining your reasoning>",
        "recommendation": "<'fire' or 'frozen'>"
    ]

    Your input will be provided as JSON data where each abstract will be associated with a search term. The search term should be the same for all abstracts.
    JSON: {text}'''

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-4o-mini-2024-07-18",  # You can change this to other models supported by OpenRouter
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        print("checkpoint 1: Before API call")
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
        print("checkpoint 2: After API call")
        response.raise_for_status()
        print("checkpoint 3: After raise_for_status")
        result = response.json()
        print("checkpoint 4: After parsing JSON")
        ai_response = result['choices'][0]['message']['content']
        print("checkpoint 5: After extracting AI response")
        # Replace 'frozen' with the frozen face emoji and 'fire' with the fire emoji
        ai_response = ai_response.replace("'frozen'", "'🥶'")
        ai_response = ai_response.replace("'fire'", "'🔥'")
        print(ai_response)
        return jsonify({"result": ai_response})
    except requests.exceptions.RequestException as e:
        print(f"checkpoint error: {str(e)}")
        return jsonify({"error": f"Error calling OpenRouter API: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)