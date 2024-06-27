import hashlib
#import streamlit as st

@st.cache_data(ttl=3600)
def cached_scrape(url):
    cache_key = hashlib.md5(url.encode()).hexdigest()
    article = scrape_full_article(url)
    return article
