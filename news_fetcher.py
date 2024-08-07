import streamlit as st
import feedparser
from huggingface_hub import login
from transformers import AutoTokenizer 
from optimum.onnxruntime import ORTModelForSeq2SeqLM
from scraper import cached_scrape
from config import rss_feeds, category_feeds
import os

# Login to Hugging Face
api_key = st.secrets["huggingface_api_key"]
login(token = api_key, add_to_git_credential=True ) 

# Load the model and tokenizer once
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("akomst6/CoD_4_1_onnx") 
    model = ORTModelForSeq2SeqLM.from_pretrained("akomst6/CoD_4_1_onnx")
    return tokenizer, model

tokenizer, model = load_model()

def fetch_news_from_rss(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        articles.append({
            'title': entry.title,
            'description': entry.get(
                'summary',
                'No summary available.'),
            'link': entry.link
        })
    return articles

def generate_summary(text):
    try:
        input_text = f"summarize: {text}"
        inputs = tokenizer.encode(
            input_text,
            return_tensors='pt',
            max_length=1200,
            truncation=True)
        outputs = model.generate(
            inputs,
            min_length=120,
            max_length=200,
            repetition_penalty=1.5)
        summary = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True)
        return summary
    except Exception as e:
        print(f"Error in generate_summary: {str(e)}")
        return None

def filter_articles(articles, search_term):
    return [article for article in articles if search_term.lower() in article['title'].lower()]

def get_articles_for_source(source, search_term=""):
    articles = fetch_news_from_rss(rss_feeds[source])
    return filter_articles(articles, search_term)

def get_sources_for_category(category):
    return category_feeds.get(category, [])

# Export the category list for use in the interface
categories = list(category_feeds.keys())
