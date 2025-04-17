import json
from datetime import datetime

from openai import OpenAI

def get_prompt(id: str) -> str:
    with open('apis/prompts.json', 'r', encoding='utf-8') as f:
        prompts: dict = json.load(f)
    return prompts[id]

def was_scraped_successfully(scraped_data: str, api_key: str) -> bool:
    client: OpenAI = OpenAI(api_key=api_key)

    model_response: str = client.chat.completions.create(
        model='gpt-4.1-nano',
        messages=[
            {
                'role': 'system',
                'content': get_prompt('check_for_successful_scrape')
            },
            {
                'role': 'user',
                'content': f'Here is the extracted story: {scraped_data}'
            }
        ]
    ).choices[0].message.content.lower()

    if 'true' in model_response:
        return True
    return False # Fallback

def gen_podcast_segment(story: str, api_key: str) -> str:
    client: OpenAI = OpenAI(api_key=api_key)

    model_response: str = client.chat.completions.create(
        model='gpt-4.1-nano',
        messages=[
            {
                'role': 'system',
                'content': get_prompt('rewrite_like_podcast')
            },
            {
                'role': 'user',
                'content': f'Here is the story: {story}'
            }
        ]
    ).choices[0].message.content

    return model_response

def compile_podcast_script(content: list[str], api_key: str) -> str:
    client: OpenAI = OpenAI(api_key=api_key)

    # Convert the segments
    news_content: str = ""
    total_stories: int = len(content)
    for i in range(len(content)):
        news_content += f"Story {str(i)} of {str(total_stories)}: {content[i]}"

    # Get the current time and round to the nearest hour
    now = datetime.now()
    rounded_hour = now.replace(minute=0, second=0, microsecond=0)
    if now.minute >= 30:
        rounded_hour = rounded_hour.replace(hour=(rounded_hour.hour + 1) % 24)

    # Format the date as "Monday, June third, 2025"
    formatted_date = rounded_hour.strftime("%A, %B")
    day = int(rounded_hour.strftime("%d"))
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    formatted_date += f" {day}{suffix}, {rounded_hour.year}"


    model_response: str = client.chat.completions.create(
        model='gpt-4.1-mini',
        messages=[
            {
                'role': 'system',
                'content': get_prompt('write_full_script')
            },
            {
                'role': 'user',
                'content': f'Here are the stories: {news_content}'
            },
            {
                'role': 'user',
                'content': f'Here is extra info to include in your response: It is {formatted_date}. The name of the podcast is "The Rundown". Your name is "Coral".'
            }
        ]
    ).choices[0].message.content

    return model_response
