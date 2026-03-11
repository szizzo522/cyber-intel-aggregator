import json
from datetime import datetime
import os
from xml.sax.saxutils import escape
import re

# Create output folder
os.makedirs("generated_feeds", exist_ok=True)

# Load articles
with open("tagged_articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# Dictionary: key=category, value=list of RSS <item>s
feeds = {}

# Safe filename helper
def safe_filename(name):
    name = name.lower().replace(" ", "_")
    name = re.sub(r"[^a-z0-9_]", "", name)
    return name or "general"

# Build RSS items
for article in articles:
    title = escape(article.get("title", "No Title"))
    link = escape(article.get("link", ""))
    summary = escape(article.get("summary", ""))
    category = article.get("tag", "General")

    # Prepend category in title for clarity
    title_with_tag = f"[{category}] {title}"

    # Format pubDate
    pub_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    # Create RSS item
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
    # Add to category-specific feed
    feeds.setdefault(category, []).append(item_xml)

# Function to build full RSS XML
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

# Write one file per category only — filenames are safe
for category_name, items in feeds.items():
    filename = f"generated_feeds/{safe_filename(category_name)}.xml"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(build_rss(items, feed_title=f"Cyber Threat Intel Feed - {category_name}"))

print("✅ RSS feeds generated successfully!")
