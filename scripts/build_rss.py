import json
from datetime import datetime
import os
from xml.sax.saxutils import escape

# Ensure the folder exists
os.makedirs("generated_feeds", exist_ok=True)

# Load tagged articles
with open("tagged_articles.json") as f:
    articles = json.load(f)

# Prepare dictionaries for category feeds
category_feeds = {}

# Build items
for a in articles:
    # Extract fields
    title = escape(a["title"])
    link = escape(a["link"])
    summary = escape(a["summary"])
    
    # Use AI-generated tag if exists (default to "General")
    category = a.get("tag", "General")
    
    # Prepend category to the title
    title_with_tag = f"[{category}] {title}"
    
    # Format pubDate
    pub_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    # Build XML for this item
    item_xml = f"""
    <item>
        <title>{title_with_tag}</title>
        <link>{link}</link>
        <description><![CDATA[{summary}]]></description>
        <pubDate>{pub_date}</pubDate>
    </item>
    """
    
    # Add to main feed
    if "all" not in category_feeds:
        category_feeds["all"] = []
    category_feeds["all"].append(item_xml)
    
    # Add to category-specific feed
    if category not in category_feeds:
        category_feeds[category] = []
    category_feeds[category].append(item_xml)

# Function to build full RSS
def build_rss(feed_items, feed_title="Cyber Threat Intel Feed"):
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>{feed_title}</title>
<link>https://isamuel.dev</link>
<description>Aggregated cybersecurity news</description>
"""
    rss += "\n".join(feed_items)
    rss += "\n</channel></rss>"
    return rss

# Write all feeds
for cat, items in category_feeds.items():
    filename = f"generated_feeds/{cat.lower().replace(' ', '_')}.xml"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(build_rss(items, feed_title=f"Cyber Threat Intel Feed - {cat}"))

print("RSS feeds generated successfully!")
