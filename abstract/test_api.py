import requests
import json

# API endpoint URL (adjust if your Flask app is running on a different port)
API_URL = "http://127.0.0.1:2000/analyze_sentiment"

def test_sentiment_analysis(text, search_term):
    payload = {
        "text": text,
        "search_term": search_term
    }
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        print(f"Input text (truncated): {text[:100]}...")
        print(f"Search term: {search_term}")
        print(f"Status code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    print("-" * 50)

# Test cases
test_cases = [
    {
        "text": "Transformers have their pros and cons but are ultimately a great tool for scientific research.",
        "search_term": "transformers"
    },
    {
        "text": "This experiment failed miserably and wasted our time and resources.",
        "search_term": "experiment"
    },
    {
        "text": "The results of the study were inconclusive, requiring further investigation.",
        "search_term": "research results"
    },
    {
        "text": "Foundation models, now powering most of the exciting applications in deep learning, are almost universally based on the Transformer architecture and its core attention module. Many subquadratic-time architectures such as linear attention, gated convolution and recurrent models, and structured state space models (SSMs) have been developed to address Transformers' computational inefficiency on long sequences, but they have not performed as well as attention on important modalities such as language.",
        "search_term": "transformer efficiency"
    },
    {
        "text": "Self-attention performs well in long context but has quadratic complexity. Existing RNN layers have linear complexity, but their performance in long context is limited by the expressive power of their hidden state. We propose a new class of sequence modeling layers with linear complexity and an expressive hidden state. The key idea is to make the hidden state a machine learning model itself, and the update rule a step of self-supervised learning. Since the hidden state is updated by training even on test sequences, our layers are called Test-Time Training (TTT) layers. We consider two instantiations: TTT-Linear and TTT-MLP, whose hidden state is a linear model and a two-layer MLP respectively. We evaluate our instantiations at the scale of 125M to 1.3B parameters, comparing with a strong Transformer and Mamba, a modern RNN. Both TTT-Linear and TTT-MLP match or exceed the baselines. Similar to Transformer, they can keep reducing perplexity by conditioning on more tokens, while Mamba cannot after 16k context. With preliminary systems optimization, TTT-Linear is already faster than Transformer at 8k context and matches Mamba in wall-clock time. TTT-MLP still faces challenges in memory I/O, but shows larger potential in long context, pointing to a promising direction for future research.",
        "search_term": "transformer"
    }
]

# Run tests
for case in test_cases:
    test_sentiment_analysis(case["text"], case["search_term"])