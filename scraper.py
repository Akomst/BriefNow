import requests
from bs4 import BeautifulSoup
import streamlit as st

def scrape_full_article(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        article_text = " ".join([para.get_text() for para in paragraphs if para.get_text()])
        return article_text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching article: {e}")
        return ""

@st.cache_data(ttl=3600)
def cached_scrape(url):
    article = scrape_full_article(url)
    return article
