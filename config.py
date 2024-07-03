# config.py

# Mapping RSS feed URLs
rss_feeds = {
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "Reuters": "http://feeds.reuters.com/reuters/topNews",
    "Guardian": "https://www.theguardian.com/world/rss",
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
    "The Nation": "https://thenationonlineng.net/feed",
    "Sahara Reporters": "https://saharareporters.com/articles/rss-feed",
    "Yahoo": "http://rss.news.yahoo.com/rss/world",
    "BBC India":"http://feeds.bbci.co.uk/news/world/asia/india/rss.xml ",
    "The Hindu": "http://www.thehindu.com/news/national/?service=rss",
    "Business Insider": "https://feeds.businessinsider.com/custom/all",
    "MIT Tech Review": "https://www.technologyreview.com/feed/",
    "Harvard Business Review": "http://feeds.hbr.org/harvardbusiness",
    "TechCrunch":"https://techcrunch.com/feed/",
    "VentureBeat":"http://feeds.feedburner.com/venturebeat/SZYF", 
    "Scientific America": "http://rss.sciam.com/ScientificAmerican-Global",
    "BusinessDay NG": "https://businessday.ng/feed/",
    "PT Business": "https://www.premiumtimesng.com/category/business/feed",
    "TheNation Business": "https://thenationonlineng.net/category/business/feed/",
    "TechCabal": "https://techcabal.com/feed/"
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
      "The Nation",
      "Sahara Reporters"],
      
    "Global": [
    "Al Jazeera", 
    "BBC", 
    "Yahoo",
    "Guardian", 
    "New York Times"],
    
    "India News": [
    "BBC India", 
    "The Hindu"],
    
    "Business News":[
    "BusinessDay NG",
    "TheNation Business",
    "PT Business", 
    "Business Insider",
    "Harvard Business Review"
    ],
    
    "Science and Technology":[
    "MIT Tech Review",
    "TechCrunch", 
    "TechCabal",
    "VentureBeat",
    "Scientific America"
    ]
    
}