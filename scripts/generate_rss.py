import feedparser
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import os
import traceback

# Ensure the output folder exists
OUTPUT_DIR = "rss"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Feeds to aggregate
FEEDS = {
    "world": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
    ],
    "usa": [
        "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
        "https://www.npr.org/rss/rss.php?id=1001"
    ],
    "florida": [
        "https://www.miamiherald.com/rss/feed/?section=Top%20Stories",
        "https://www.tampabay.com/rss/topnews/"
    ],
    "cyber": [
        "https://www.crowdstrike.com/blog/feed/",
        "https://www.ibm.com/blogs/security/feed/",
        "https://www.tanium.com/blog/feed/",
        "https://www.gartner.com/en/newsroom/rss-feeds",
        "https://www.lapsus.com/feed/"  # hypothetical
    ]
}

def generate_rss(feed_name, urls):
    """Generate an aggregated RSS feed."""
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = f"{feed_name.capitalize()} RSS Feed"
    ET.SubElement(channel, "link").text = "https://isamuel.dev/rss-feed/"
    ET.SubElement(channel, "description").text = f"Aggregated {feed_name} news feed."
    ET.SubElement(channel, "lastBuildDate").text = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

    for url in urls:
        try:
            d = feedparser.parse(url)
            for entry in d.entries[:10]:  # latest 10 articles per feed
                item = ET.SubElement(channel, "item")
                ET.SubElement(item, "title").text = entry.get("title", "No title")
                ET.SubElement(item, "link").text = entry.get("link", url)
                # Some feeds use 'summary', others 'description'
                ET.SubElement(item, "description").text = entry.get("summary", entry.get("description", ""))
                ET.SubElement(item, "pubDate").text = entry.get(
                    "published",
                    datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
                )
        except Exception as e:
            print(f"Failed to parse feed {url}: {e}")
            traceback.print_exc()  # keep running even if one feed fails

    # Safe filename
    safe_name = "".join(c if c.isalnum() else "_" for c in feed_name)
    filename = os.path.join(OUTPUT_DIR, f"{safe_name}.xml")
    tree = ET.ElementTree(rss)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"Generated {filename}")

# Generate all feeds
for feed_name, urls in FEEDS.items():
    generate_rss(feed_name, urls)
