import requests

API_KEY = "your_api_key"
url = "https://newsapi.org/v2/top-headlines"
params = {
    "country": "us",         # Change to desired region
    "pageSize": 5,           # Limit to top 5
    "apiKey": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

top_stories = [(a["title"], a["url"]) for a in data["articles"]]
for i, (title, link) in enumerate(top_stories, 1):
    print(f"{i}. {title}\n   {link}\n")
