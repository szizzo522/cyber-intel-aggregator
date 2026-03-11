import json
from datetime import datetime

with open("tagged_articles.json") as f:
    articles = json.load(f)

rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>Cyber Threat Intel Feed</title>
<link>https://isamuel.dev</link>
<description>Aggregated cybersecurity news</description>
"""

for a in articles:
    rss += f"""
    <item>
    <title>{a['title']}</title>
    <link>{a['link']}</link>
    <description>{a['summary']}</description>
    <pubDate>{datetime.utcnow()}</pubDate>
    </item>
    """

rss += "</channel></rss>"

with open("generated_feeds/all.xml","w") as f:
    f.write(rss)
