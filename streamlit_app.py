import streamlit as st
from streamlit_auth0 import login_button
from news_fetcher import get_articles_for_source, get_sources_for_category, generate_summary, categories
from pymongo import MongoClient
from scraper import cached_scrape

# Set page config at the very beginning
st.set_page_config(page_title="BriefNow", layout="wide")

st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .title {
        font-size: 3em; 
        font-weight: bold; 
        text-align: center; 
        margin-top: 0; 
        padding-top: 0;
        color: #ffc107;
    }
    .subtitle {
        font-size: 1.5em; 
        text-align: center; 
        color: #e0e0e0; 
        margin-bottom: 2em;
    }
    .footer {
        font-size: 0.8em; 
        text-align: center; 
        color: grey; 
        margin-top: 2em; 
        margin-bottom: 1em; 
        padding-top: 1em; 
        border-top: 1px solid #e6e6e6;
    }
    .article-card {
        background-color: #f0f0f0;
        border-radius: 20px;
        padding: 5px;
        margin-bottom: 0em;
        transition: all 0.3s ease;
    }
    .article-card:hover {
        background-color: #e0e0e0;
    }
    .article-title {
        font-size: 1.8em;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5em;
    }
    .article-description {
        font-size: 1em;
        color: #555;
        margin-bottom: 1em;
    }
    .action-icons {
        display: flex;
        justify-content: flex-start;
        align-items: center;
        flex-wrap: nowrap;
    }
    .action-icon {
        margin-right: 15px;
        cursor: pointer;
        font-size: 20px;
    }
    .share-icon { color: #1DA1F2; }
    .summary-icon { color: #4CAF50; }
    .menu-icon { color: #333; }
    .summary-container {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 0.5px;
        padding: 15px;
        margin-top: 0.5px;
    }
    .summary-title {
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 10px;
        color: #333;
    }
    .summary-text {
        font-size: 1em;
        line-height: 1.5;
        color: #444;
    }
    .pagination-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 1em;
    }
    .pagination-button {
        flex-basis: 45%;
        margin: 0.5em;
    }
    .pagination-button button {
        width: 100%;
        padding: 0.5em 1em;
    }
    @media (max-width: 600px) {
        .pagination-container {
            flex-direction: row;
            justify-content: space-between;
        }
        .pagination-button {
            flex-basis: 45%;
            margin: 0.5em;
        }
        .pagination-button button {
            width: 100%;
            padding: 4em 3em;
        }
        /* Added styles for button positioning  */
        col1 .pagination-button,
        col3 .pagination-button {
            justify-content: flex-end;
            color: red;
        }
    }
    </style>
""", unsafe_allow_html=True)

username = st.secrets["mongodb_username"]
password = st.secrets["mongodb_password"]

# Construct the Mongo URI
MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.l1n4uzh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
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

def get_bookmarked_articles(user_info):
    if user_info:
        bookmarks = bookmarks_collection.find({"user_id": user_info["sub"]})
        return [bookmark["article"] for bookmark in bookmarks]
    return []

def display_article(article, source, page, index, user_info):
    with st.container():
        st.markdown(f'<div class="article-card">', unsafe_allow_html=True)
        st.markdown(f'<a href="{article["link"]}" target="_blank"><h2 class="article-title">{article["title"]}</h2></a>', unsafe_allow_html=True)
        st.markdown(f'<p class="article-description">{article["description"][:200]}...</p>', unsafe_allow_html=True)
        
        st.markdown('<div class="action-icons">', unsafe_allow_html=True)
        st.markdown('<span class="action-icon share-icon" title="Share">&#128279;</span>', unsafe_allow_html=True)
        summary_key = f"summary_{source}_{page}_{index}_{article['link']}"
        bookmark_key = f"bookmark_{source}_{page}_{index}_{article['link']}"
        if st.button("Summary", key=summary_key, help="Generate a summary of the article"):
            with st.spinner('Generating summary...'):
                full_text = cached_scrape(article['link'])
                summary = generate_summary(full_text)
                st.markdown('<div class="summary-container">', unsafe_allow_html=True)
                st.markdown('<div class="summary-title">Article Summary</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="summary-text">{summary}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Bookmark", key=bookmark_key, help="Bookmark this article"):
            bookmark_article(user_info, article)
        st.markdown('<span class="action-icon menu-icon" title="More options">&#8942;</span>', unsafe_allow_html=True)
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

def display_news_for_category(category, user_info):
    sources = get_sources_for_category(category)
    search_term = st.text_input("Search headlines:", key=f"search_{category}")
    
    tabs = st.tabs(sources)
    for i, source in enumerate(sources):
        with tabs[i]:
            display_paginated_news(source, search_term, 10, user_info)

def main():
    st.sidebar.title("BriefNow")
    st.sidebar.subheader("Choose a News Source")
    selected_category = st.sidebar.selectbox("Choose a category:", ["All"] + categories)

    st.markdown('<div class="title">BriefNow</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Stay Informed, Stay Brief</div>', unsafe_allow_html=True)

    client_id = st.secrets["auth0_client_id"]
    domain = st.secrets["auth0_domain"]

    user_info = login_button(client_id=client_id, domain=domain)
    
    if user_info:
        st.sidebar.success(f"Logged in as {user_info['name']}")
        if st.sidebar.button("View Bookmarked Articles"):
            bookmarks = get_bookmarked_articles(user_info)
            st.write("## Bookmarked Articles")
            for article in bookmarks:
                display_article(article, "bookmarked", 0, 0, user_info)
    else:
        st.sidebar.info("Please log in to access more features.")

    if selected_category == "All":
        st.info("Please select a specific category to view news.")
    else:
        display_news_for_category(selected_category, user_info)

    st.markdown('<div class="footer">Powered by BriefNow</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
