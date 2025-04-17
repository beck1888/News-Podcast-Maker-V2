import requests

def get_top_stories(api_key: int, number_of_stories: int = 5, region: str = 'us') -> list[str]:
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": region,
        "pageSize": number_of_stories,
        "apiKey": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    top_stories = [(a["title"], a["url"]) for a in data["articles"]]

    return top_stories
