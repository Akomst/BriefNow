import streamlit as st
from streamlit_auth0 import login_button
from news_fetcher import get_articles_for_source, get_sources_for_category, generate_summary, categories
from pymongo import MongoClient
from scraper import cached_scrape
import certifi

# Set page config at the very beginning
st.set_page_config(page_title="BriefNow", layout="wide")

# MongoDB setup
username = st.secrets["mongodb_username"]
password = st.secrets["mongodb_password"]
MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.l1n4uzh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
ca = certifi.where()
client = MongoClient(MONGO_URI, tlsCAFile=ca)
db = client["BriefNow"]
bookmarks_collection = db["bookmarks"]

def bookmark_article(user_info, article):
    if user_info:
        bookmark = {
            "user_id": user_info["sub"],
            "article": article
        }
        bookmarks_collection.update_one(
            {"user_id": user_info["sub"], "article.link": article["link"]},
            {"$set": bookmark},
            upsert=True
        )
        st.success("Article bookmarked!")
    else:
        st.info("Please log in to bookmark articles.")

def remove_bookmark(user_info, article):
    if user_info:
        bookmarks_collection.delete_one(
            {"user_id": user_info["sub"], "article.link": article["link"]}
        )
        st.success("Article removed from bookmarks!")
    else:
        st.info("Please log in to manage bookmarks.")

def get_bookmarked_articles(user_info):
    if user_info:
        bookmarks = bookmarks_collection.find({"user_id": user_info["sub"]})
        return [bookmark["article"] for bookmark in bookmarks]
    return []

def filter_articles(articles, search_term):
    return [article for article in articles if search_term.lower() in article['title'].lower() or search_term.lower() in article['description'].lower()]

def display_article(article, source, page, index, user_info, is_bookmarked=False):
    with st.container():
        st.markdown(f'<div class="article-card">', unsafe_allow_html=True)
        st.markdown(f'<a href="{article["link"]}" target="_blank" class="article-title">{article["title"]}</a>', unsafe_allow_html=True)
        st.markdown(f'<p class="article-description">{article["description"][:200]}...</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        summary_key = f"summary_{source}_{page}_{index}_{article['link']}"
        action_key = f"action_{source}_{page}_{index}_{article['link']}"
        
        with col1:
            if st.button("Summary", key=summary_key, help="Generate a summary of the article"):
                st.session_state[f"show_summary_{summary_key}"] = True
        
        with col2:
            if is_bookmarked:
                if st.button("Remove", key=action_key, help="Remove this article from bookmarks"):
                    remove_bookmark(user_info, article)
                    st.experimental_rerun()
            else:
                if st.button("Bookmark", key=action_key, help="Bookmark this article"):
                    bookmark_article(user_info, article)

        # Display summary in a separate container below the buttons
        if st.session_state.get(f"show_summary_{summary_key}", False):
            with st.spinner('Generating summary...'):
                full_text = cached_scrape(article['link'])
                summary = generate_summary(full_text)
                st.markdown('<div class="summary-container">', unsafe_allow_html=True)
                st.markdown('<div class="summary-title">Article Summary</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="summary-text">{summary}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

def display_paginated_news(source, search_term, items_per_page, user_info):
    articles = get_articles_for_source(source, search_term)
    
    # Initialize session state for pagination
    if f'{source}_page' not in st.session_state:
        st.session_state[f'{source}_page'] = 0

    page = st.session_state[f'{source}_page']
    start = page * items_per_page
    end = start + items_per_page
    
    for index, article in enumerate(articles[start:end], start=start):
        display_article(article, source, page, index, user_info)
    
    total_pages = (len(articles) - 1) // items_per_page + 1
    
    st.markdown('<div class="pagination-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown('<div class="pagination-button">', unsafe_allow_html=True)
        if st.button("Previous", key=f"prev_{source}_{page}", disabled=(page == 0)):
            st.session_state[f'{source}_page'] -= 1
            st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.write(f"Page {page + 1} of {total_pages}")
    with col3:
        st.markdown('<div class="pagination-button">', unsafe_allow_html=True)
        if st.button("Next", key=f"next_{source}_{page}", disabled=(page + 1 >= total_pages)):
            st.session_state[f'{source}_page'] += 1
            st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def display_bookmarked_articles(user_info, search_term=""):
    bookmarks = get_bookmarked_articles(user_info)
    filtered_bookmarks = filter_articles(bookmarks, search_term) if search_term else bookmarks
    if filtered_bookmarks:
        for index, article in enumerate(filtered_bookmarks):
            display_article(article, "bookmarked", 0, index, user_info, is_bookmarked=True)
    else:
        st.info("No matching bookmarked articles found." if search_term else "You haven't bookmarked any articles yet.")

def display_news_for_category(category, user_info, search_term=""):
    sources = get_sources_for_category(category)
    
    tabs = st.tabs(sources)
    for i, source in enumerate(sources):
        with tabs[i]:
            display_paginated_news(source, search_term, 10, user_info)

def main():
    st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .title {
        font-size: 2.5em; 
        font-weight: bold; 
        text-align: center; 
        margin-top: 0.5em; 
        padding-top: 0;
        color: #ffc107;
    }
    .subtitle {
        font-size: 1.2em; 
        text-align: center; 
        color: #e0e0e0; 
        margin-bottom: 1em;
    }
    .footer {
        font-size: 0.8em; 
        text-align: center; 
        color: grey; 
        margin-top: 1em; 
        margin-bottom: 0.5em; 
        padding-top: 0.5em; 
        border-top: 1px solid #e6e6e6;
    }
    .article-card {
        background-color: #f0f0f0;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 0.5em;
        transition: all 0.3s ease;
    }
    .article-card:hover {
        background-color: #e0e0e0;
    }
    .article-title {
        font-size: 1.4em;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.3em;
        text-decoration: none;
    }
    .article-title:hover {
        text-decoration: underline;
    }
    .article-description {
        font-size: 0.9em;
        color: #555;
        margin-bottom: 0.7em;
    }
    .summary-container {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 15px;
        margin-top: 10px;
        width: 100%;
    }
    .summary-title {
        font-size: 1.1em;
        font-weight: bold;
        margin-bottom: 10px;
        color: #333;
    }
    .summary-text {
        font-size: 0.9em;
        line-height: 1.4;
        color: #444;
    }
    .stTextInput > div > div > input {
        color: #4a4a4a;
    }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("BriefNow")
    st.sidebar.subheader("Choose a News Source")
    
    st.markdown('<div class="title">BriefNow</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Stay Informed, Stay Brief</div>', unsafe_allow_html=True)

    client_id = st.secrets["auth0_client_id"]
    domain = st.secrets["auth0_domain"]
        
    # Create a row for search box and login button
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_term = st.text_input("", placeholder="Search articles...", key="global_search")
    
    with col2:
        user_info = login_button(client_id=client_id, domain=domain, key="login_button")

    if user_info:
        st.sidebar.success(f"Logged in as {user_info['name']}")
    else:
        st.sidebar.info("Please log in to access more features.")

    # Create tabs for "News" and "Bookmarks"
    news_tab, bookmarks_tab = st.tabs(["News", "Bookmarks"])

    with news_tab:
        selected_category = st.selectbox("Choose a category:", ["All"] + categories)

        if selected_category == "All":
            st.info("Please select a specific category to view news.")
        else:
            display_news_for_category(selected_category, user_info, search_term)

    with bookmarks_tab:
        if user_info:
            display_bookmarked_articles(user_info, search_term)
        else:
            st.info("Please log in to view your bookmarked articles.")

    st.markdown('<div class="footer">Powered by BriefNow</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
