import requests
import json
import os
import time

# Load API key from environment
API_KEY = os.environ["OPENROUTER_API_KEY"]

# Load articles collected by collect.py
with open("articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

tagged = []

for a in articles:
    # Prepare the prompt for the AI
    prompt = f"""
Categorize this cybersecurity article.

Return ONLY JSON with:
{{"category": one of ["ransomware", "vulnerability", "malware", "threat-intel", "general"]}}

Title: {a['title']}
Summary: {a.get('summary','')}
"""

    # Send request to OpenRouter
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "anthropic/claude-3-haiku",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    result = r.json()

    # Safely parse the AI response as JSON
    raw_content = result["choices"][0]["message"]["content"].strip()
    try:
        parsed = json.loads(raw_content)
        category = parsed.get("category", "general")
    except json.JSONDecodeError:
        # fallback in case AI returned text instead of JSON
        category = "general"

    # Normalize the category to lowercase for safety
    a["tag"] = category.lower()

    tagged.append(a)

    # Optional: small delay to prevent rate limits
    time.sleep(1)

# Write the tagged articles safely
with open("tagged_articles.json", "w", encoding="utf-8") as f:
    json.dump(tagged, f, ensure_ascii=False, indent=2)

print("✅ Articles tagged successfully!")
