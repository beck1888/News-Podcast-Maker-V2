import json
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
