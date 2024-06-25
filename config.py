# config.py

# Mapping RSS feed URLs
rss_feeds = {
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "CNN": "http://rss.cnn.com/rss/edition.rss",
    "Reuters": "http://feeds.reuters.com/reuters/topNews",
    "The Guardian": "https://www.theguardian.com/world/rss",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "New York Times": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
}

# Mapping categories to RSS feeds
category_feeds = {
    "Sports": ["BBC", "CNN"],
    "Entertainment": ["Reuters", "The Guardian"],
    "Politics": ["Al Jazeera", "New York Times"],
    "Business": ["Reuters", "New York Times"],
    "Local": ["The Guardian"],
    "Regional": ["Al Jazeera"],
    "Global": ["BBC", "CNN"]
}
