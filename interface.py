import streamlit as st
from news_fetcher import get_articles_for_source, get_sources_for_category, generate_summary, categories
from scraper import cached_scrape

# Set page config at the very beginning
st.set_page_config(page_title="BriefNow", layout="wide")

# Custom CSS
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
    .pagination-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 1em;
        background-color: #ffcccb; /* Debug color for large screens */
    }
    .pagination-button {
        min-width: 100px;
        background-color: #d4edda; /* Debug color for large screens */
    }
    .pagination-button button {
        width: 100%;
        padding: 0.5em 1em; 
    }
    @media (max-width: 600px) {
        .pagination-container {
            background-color: yellow; /* Debug color for small screens */
            justify-content: space-between; 
            align-items: center; 
            flex-direction: row; /* Ensure buttons are in a row */
        }
        .pagination-button {
            background-color: blue; /* Debug color for small screens */
            flex: 1;
            margin: 0 5px; /* Adjust margin for spacing */
        }
        .pagination-button button {
            width: 100%;
            padding: 0.5em 1em; 
        }
    }
    </style>
""", unsafe_allow_html=True)
# Custom CSS
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
    .pagination-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 1em;
        background-color: #ffcccb; /* Debug color for large screens */
    }
    .pagination-button {
        min-width: 100px;
        background-color: #d4edda; /* Debug color for large screens */
    }
    .pagination-button button {
        width: 100%;
        padding: 0.5em 1em; 
    }
    @media (max-width: 600px) {
        .pagination-container {
            background-color: yellow; /* Debug color for small screens */
            justify-content: space-between; 
            align-items: center; 
            flex-direction: row; /* Ensure buttons are in a row */
        }
        .pagination-button {
            background-color: blue; /* Debug color for small screens */
            flex: 1;
            margin: 0 5px; /* Adjust margin for spacing */
        }
        .pagination-button button {
            width: 100%;
            padding: 0.5em 1em; 
        }
    }
    </style>
""", unsafe_allow_html=True)



def display_article(article, source, page, index):
    with st.container():
        st.markdown(f'<div class="article-card">', unsafe_allow_html=True)
        st.markdown(f'<h2 class="article-title">{article["title"]}</h2>', unsafe_allow_html=True)
        st.markdown(f'<p class="article-description">{article["description"][:200]}...</p>', unsafe_allow_html=True)
        
        st.markdown('<div class="action-icons">', unsafe_allow_html=True)
        st.markdown('<span class="action-icon share-icon" title="Share">&#128279;</span>', unsafe_allow_html=True)
        if st.button("Summary", key=f"summary_{source}_{page}_{index}", help="Generate a summary of the article"):
            with st.spinner('Generating summary...'):
                full_text = cached_scrape(article['link'])
                summary = generate_summary(full_text)
                st.markdown('<div class="summary-container">', unsafe_allow_html=True)
                st.markdown('<div class="summary-title">Article Summary</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="summary-text">{summary}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<span class="action-icon menu-icon" title="More options">&#8942;</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

def display_paginated_news(source, search_term="", items_per_page=10):
    articles = get_articles_for_source(source, search_term)
    
    # Initialize session state for pagination
    if f'{source}_page' not in st.session_state:
        st.session_state[f'{source}_page'] = 0

    page = st.session_state[f'{source}_page']
    start = page * items_per_page
    end = start + items_per_page
    
    for index, article in enumerate(articles[start:end], start=start):
        display_article(article, source, page, index)
    
    total_pages = (len(articles) - 1) // items_per_page + 1
    
    st.markdown('<div class="pagination-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
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

def display_news_for_category(category):
    sources = get_sources_for_category(category)
    search_term = st.text_input("Search headlines:", key=f"search_{category}")
    
    tabs = st.tabs(sources)
    for i, source in enumerate(sources):
        with tabs[i]:
            display_paginated_news(source, search_term)

def main():
    st.sidebar.title("BriefNow")
    st.sidebar.subheader("Choose a News Source")
    selected_category = st.sidebar.selectbox("Choose a category:", ["All"] + categories)

    st.markdown('<div class="title">BriefNow</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Stay Informed, Stay Brief</div>', unsafe_allow_html=True)

    if selected_category == "All":
        st.info("Please select a specific category to view news.")
    else:
        display_news_for_category(selected_category)

    st.markdown('<div class="footer">Powered by BriefNow</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
