from apis.fetch_news import get_top_stories
from apis.scrape import scrape_page
from tools.environment_manager import get_environmental_variable
from tools.terminal import spinner

def main() -> None:
    # Load in API keys
    with spinner('Setting up environment'):
        news_api_key: str = get_environmental_variable('NEWSAPI_API_KEY')
        openai_api_key: str = get_environmental_variable('OPENAI_API_KEY')

    # Start by fetching the news
    with spinner('Getting top stories'):
        news: list[str] = get_top_stories(news_api_key)

    # Collect output
    headlines: dict = {}
    for index, story in enumerate(news, start=1):
        with spinner(f'Reading story {str(index)} of 5'):
            url = story[1]
            headlines[index] = {
                'headline': story[0],
                'story': scrape_page(url)
            }

    print(headlines)




if __name__ == '__main__':
    main()
