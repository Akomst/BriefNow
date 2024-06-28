# config.py

# Mapping RSS feed URLs
rss_feeds = {
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "CNN": "http://rss.cnn.com/rss/edition.rss",
    "Reuters": "http://feeds.reuters.com/reuters/topNews",
    "The Guardian": "https://www.theguardian.com/world/rss",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "New York Times": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "The Guardian": "https://guardian.ng/feed/",
    "Premium Times": "https://www.premiumtimesng.com/feed",
    "Punch": "https://punchng.com/feed/",
    "ThisDay": "https://www.thisdaylive.com/index.php/feed/",
    "Leadership": "https://leadership.ng/feed/",
    "Tribune": "https://tribuneonlineng.com/feed/",
    "DailyNigeria": "https://dailynigerian.com/feed/",
    "The Herald": "https://www.herald.ng/feed/",
    "The Gazette": "https://thegazettengr.com/feed/",
    "Vanguard": "https://www.vanguardngr.com/feed/",
    "The Nation": "https://thenationonlineng.net/feed",
    "Sahara Reporters": "https://saharareporters.com/articles/rss-feed",
    "Yahoo": "http://rss.news.yahoo.com/rss/world",
    "BBC India":"http://feeds.bbci.co.uk/news/world/asia/india/rss.xml ",
    "The Hindu": "http://www.thehindu.com/news/national/?service=rss",
    "Times of India": "http://timesofindia.feedsportal.com/c/33039/f/533965/index.rss "
}


# Mapping categories to RSS feeds
category_feeds = {
    "Nigeria":[
    "The Guardian",
     "Premium Times", 
     "Punch", 
     "ThisDay",
      "Leadership", 
      "Tribune",
      "DailyNigeria", 
      "The Herald",
      "The Gazette",
      "Vanguard", 
      "The Nation",
      "Sahara Reporters"],
      
    "Global": [
    "Al Jazeera", 
    "BBC", 
    "Yahoo",
    "CNN", 
    "The Guardian", 
    "New York Times",  
    "Guardian"],
    
    "India News": [
    "BBC India",
    "Times of India", 
    "The Hindu"]
    
}