from flask import Flask, request, jsonify
import requests
import os
import praw
from dotenv import load_dotenv
import time

from config.app import app

# Load environment variables
load_dotenv()

# OpenRouter API endpoint and key
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = "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" #os.getenv("OPENROUTER_API_KEY")
model = "anthropic/claude-3.5-sonnet" #"openai/o1-mini-2024-09-12"  #"meta-llama/llama-3.1-8b-instruct:free" #"nousresearch/hermes-3-llama-3.1-405b:free"

# Reddit API setup
reddit = praw.Reddit(
    client_id="mh9ybXeJtdfWFp0iU7WFpQ",
    client_secret="OPvVJETUpO8Q-gXXtfnL3AhvKYg-ig",
    user_agent="hophacks2024"
)

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable is not set")

def fetch_reddit_posts(keyword, limit=2):
    subreddit = reddit.subreddit('all')
    posts = []
    for submission in subreddit.search(keyword, limit=limit):
        posts.append(submission.title)
    return posts

def analyze_sentiment(text, search_term):
    prompt = f'''Analyze the sentiment of the following text with respect to the search term. 
    Provide a sentiment score between -1 (most negative) and 1 (most positive).
    Respond with only a numeric score between -1 and 1.

    Text: {text}
    Search Term: {search_term}'''

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "seed": 42
    }

    response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    
    sentiment_text = result['choices'][0]['message']['content'].strip()
    try:
        return float(sentiment_text)
    except ValueError:
        return None

