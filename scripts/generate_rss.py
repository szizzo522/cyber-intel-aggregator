import feedparser
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import os
import traceback
import requests

OUTPUT_DIR = "rss"
os.makedirs(OUTPUT_DIR, exist_ok=True)

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
        "https://www.tanium.com/blog/feed/"
    ]
}

def fetch_feed(url):
    """Fetch RSS with timeout to prevent hanging."""
    try:
        print(f"Fetching {url}")
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return feedparser.parse(r.content)
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def generate_rss(feed_name, urls):
    print(f"\nGenerating feed: {feed_name}")

    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = f"{feed_name.capitalize()} RSS Feed"
    ET.SubElement(channel, "link").text = "https://isamuel.dev/rss-feed/"
    ET.SubElement(channel, "description").text = f"Aggregated {feed_name} news feed."
    ET.SubElement(channel, "lastBuildDate").text = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

    total_items = 0

    for url in urls:
        try:
            d = fetch_feed(url)

            if not d:
                continue

            for entry in d.entries[:5]:  # limit per feed
                item = ET.SubElement(channel, "item")

                ET.SubElement(item, "title").text = entry.get("title", "No title")
                ET.SubElement(item, "link").text = entry.get("link", url)

                ET.SubElement(item, "description").text = entry.get(
                    "summary",
                    entry.get("description", "")
                )

                ET.SubElement(item, "pubDate").text = entry.get(
                    "published",
                    datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
                )

                total_items += 1

        except Exception as e:
            print(f"Failed parsing {url}: {e}")
            traceback.print_exc()

    filename = os.path.join(OUTPUT_DIR, f"{feed_name}.xml")
    tree = ET.ElementTree(rss)
    tree.write(filename, encoding="utf-8", xml_declaration=True)

    print(f"Generated {filename} with {total_items} items")

for feed_name, urls in FEEDS.items():
    generate_rss(feed_name, urls)

print("\nRSS generation complete.")