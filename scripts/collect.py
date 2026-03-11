import feedparser
import json

with open("sources/feeds.json") as f:
    sources = json.load(f)

articles = []

for src in sources:
    feed = feedparser.parse(src)

    for entry in feed.entries[:10]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.get("summary","")
        })

with open("articles.json","w") as f:
    json.dump(articles,f)
