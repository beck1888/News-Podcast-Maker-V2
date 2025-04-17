from apis.fetch_news import get_top_stories
from apis.scrape import scrape_page
from apis.text_gen import was_scraped_successfully, gen_podcast_segment, compile_podcast_script
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
    collected_news: dict = {}
    for index, story in enumerate(news, start=1):
        with spinner(f'Reading story {str(index)} of 5'):
            url = story[1]
            collected_news[index] = {
                'headline': story[0],
                'story': scrape_page(url)
            }

    # Build and validate list of stories
    final_news: list[str] = []
    for index in range(len(collected_news)):
        index = index + 1 # Start at one because I did something goofy with the last code block to make it more clear in the terminal ui
        with spinner(f'Validating scrape {str(index)} of 5'):
            headline: str = collected_news[index]['headline']
            story: str = collected_news[index]['story']
            is_scrape_sucsessful: bool = was_scraped_successfully(story, openai_api_key)
            if is_scrape_sucsessful:
                final_news.append(f'Headline: {headline.upper()} ---- Article body: {story}')
        # print(f"Scrape sucsess? {str(is_scrape_sucsessful)}")
    final_story_count: int = len(final_news)
    print(f"[INFO] {str(final_story_count)} of 5 stories are avaliable.")
    
    # Write stories like proper articles segment-by-segment
    podcast_segments: list[str] = []
    for i in range(final_story_count):
        with spinner(f'Writing segment {str(i+1)} of {str(final_story_count)}'):
            podcast_segments.append(gen_podcast_segment(final_news[i], openai_api_key))

    # Write final script
    final_script: str = ""
    with spinner('Writing final script'):
        final_script = compile_podcast_script(podcast_segments, openai_api_key)
    print(final_script)

if __name__ == '__main__':
    main()
