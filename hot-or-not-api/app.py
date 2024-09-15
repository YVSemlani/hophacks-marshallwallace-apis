import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from fetch_recent_arxiv_papers import get_recent_papers

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

OPENROUTER_API_KEY = "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" #os.getenv('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def create_json(search_term):
    abstracts = get_recent_papers(search_term)
    json = {
        "abstracts": abstracts,
        "search_term": search_term
    }
    return json

@app.route('/hot-or-not', methods=['POST'])
def hot_or_not():
    data = request.json
    if not data or 'search_term' not in data:
        return jsonify({"error": "No text provided"}), 400

    text = create_json(data['search_term'])
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
        "model": "google/gemini-flash-8b-1.5-exp",  # You can change this to other models supported by OpenRouter
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
        return jsonify({"result": ai_response})
    except requests.exceptions.RequestException as e:
        print(f"checkpoint error: {str(e)}")
        return jsonify({"error": f"Error calling OpenRouter API: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=2021)