from apis.fetch_news import get_top_stories
from tools.environment_manager import get_environmental_variable

def main() -> None:
    # Load in API keys
    news_api_key: str = get_environmental_variable('NEWSAPI_API_KEY')
    openai_api_key: str = get_environmental_variable('OPENAI_API_KEY')

    # Start by fetching the news
    news: list[str] = get_top_stories(news_api_key)

    # Collect output
    headlines: dict = {}
    for index, story in enumerate(news, start=1):
        headlines[index] = {
            'headline': story[0],
            'url': story[1]
        }




if __name__ == '__main__':
    main()
