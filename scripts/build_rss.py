import json
from datetime import datetime
import os
from xml.sax.saxutils import escape
import re

# Ensure output folder exists
os.makedirs("generated_feeds", exist_ok=True)

# Load tagged articles
with open("tagged_articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# Dictionary to hold RSS items by category
feeds = {}

# Helper function to create safe filenames from category names
def safe_filename(name):
    name = name.lower().replace(" ", "_")
    name = re.sub(r"[^a-z0-9_]", "", name)
    return name or "general"

# Process each article
for a in articles:
    title = escape(a.get("title", "No Title"))
    link = escape(a.get("link", ""))
    summary = escape(a.get("summary", ""))
    category = a.get("tag", "General")
    
    pub_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    title_with_tag = f"[{category}] {title}"

    item_xml = f"""
    <item>
        <title>{title_with_tag}</title>
        <link>{link}</link>
        <description><![CDATA[{summary}]]></description>
        <pubDate>{pub_date}</pubDate>
    </item>
    """
    
    # Add to "all" feed
    feeds.setdefault("all", []).append(item_xml)
    # Add to category feed
    feeds.setdefault(category, []).append(item_xml)

# Function to generate RSS XML
def build_rss(items, feed_title="Cyber Threat Intel Feed"):
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>{feed_title}</title>
<link>https://isamuel.dev</link>
<description>Aggregated cybersecurity news</description>
"""
    rss += "\n".join(items)
    rss += "\n</channel></rss>"
    return rss

# Write one file per category
for cat, items in feeds.items():
    filename = f"generated_feeds/{safe_filename(cat)}.xml"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(build_rss(items, feed_title=f"Cyber Threat Intel Feed - {cat}"))

print("RSS feeds generated successfully!")
