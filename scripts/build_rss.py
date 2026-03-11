import json
from datetime import datetime
import os
from xml.sax.saxutils import escape
import re

# Ensure the output folder exists
os.makedirs("generated_feeds", exist_ok=True)

# Load AI-tagged articles
with open("tagged_articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# Dictionary to hold feeds by category
category_feeds = {}

# Helper: convert category to a safe filename
def safe_filename(name):
    """
    Lowercase, replace spaces with underscores,
    remove all non-alphanumeric/underscore characters.
    Defaults to 'general' if empty.
    """
    name = name.lower().replace(" ", "_")
    name = re.sub(r"[^a-z0-9_]", "", name)
    return name or "general"

# Build RSS items
for a in articles:
    title = escape(a.get("title", "No Title"))
    link = escape(a.get("link", ""))
    summary = escape(a.get("summary", ""))
    
    # Use AI-generated tag, default to General
    category = a.get("tag", "General")
    
    # Add category to title
    title_with_tag = f"[{category}] {title}"
    
    # Format pubDate in RFC 822
    pub_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    # Create RSS item XML
    item_xml = f"""
    <item>
        <title>{title_with_tag}</title>
        <link>{link}</link>
        <description><![CDATA[{summary}]]></description>
        <pubDate>{pub_date}</pubDate>
    </item>
    """
    
    # Add to "all" feed
    category_feeds.setdefault("all", []).append(item_xml)
    
    # Add to category-specific feed
    category_feeds.setdefault(category, []).append(item_xml)

# Function to build full RSS XML
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

# Write feeds to generated_feeds folder
for cat, items in category_feeds.items():
    filename = f"generated_feeds/{safe_filename(cat)}.xml"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(build_rss(items, feed_title=f"Cyber Threat Intel Feed - {cat}"))

print("RSS feeds generated successfully!")
