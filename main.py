from apis.fetch_news import get_top_stories
from apis.scrape import scrape_page
from apis.text_gen import was_scraped_successfully, gen_podcast_segment, compile_podcast_script, parse_script
from apis.create_audio import gen_speech
from tools.environment_manager import get_environmental_variable
from tools.terminal import spinner
from pydub import AudioSegment
from datetime import datetime
import os

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
    with spinner('Writing final script'):
        final_script: str = compile_podcast_script(podcast_segments, openai_api_key)

    # Generate audio from the final script
    final_segments: list[str] = parse_script(final_script)
    audio_files: list[str] = []
    host_voice_names_in_api: list[str] = ['coral', 'onyx'] # Coral is Julia and reads odd paragraphs while Onyx is Knox in reads even paragraphs
    for index, segment in enumerate(final_segments):
        with spinner(f'Creating audio segment {str(index + 1)} of {len(final_segments)}'):
            # Get voice based on paragrpah oddness
            if index % 2 == 1:
                use_voice = 'coral'
            else:
                use_voice = 'onyx'
            audio_files.append(gen_speech(segment, openai_api_key, voice=use_voice))
    print(audio_files)
    
    # Stitch and mix audio
    def load_audio(filename: str) -> AudioSegment:
        return AudioSegment.from_file(filename)
    
    def overlay_music_with_fade(voice: AudioSegment, music: AudioSegment) -> AudioSegment:
        # Make music quieter and apply fade
        music = music - 20  # lower volume
        result = AudioSegment.silent(duration=0)
        while len(result) < len(voice):
            loop = music.fade_in(2000).fade_out(2000)
            result += loop
        return voice.overlay(result[:len(voice)])
    
    def stitch_audio_files(file_paths: list[str]) -> AudioSegment:
        combined = AudioSegment.empty()
        for path in file_paths:
            combined += load_audio(path)
        return combined
    
    def export_final_podcast(audio_files: list[str]) -> None:
        stitched_voice = stitch_audio_files(audio_files)
        music = load_audio("public/music.mp3")
        voice_with_music = overlay_music_with_fade(stitched_voice, music)
    
        final_mix = AudioSegment.empty()
        final_mix += load_audio("public/ai_notice.mp3")
        final_mix += AudioSegment.silent(duration=1000)
        final_mix += load_audio("public/intro.mp3")
        final_mix += voice_with_music
        final_mix += load_audio("public/outro.mp3")
    
        timestamp = datetime.now().strftime("%B %d at %I%p - %Y")
        output_path = os.path.join("podcasts", f"{timestamp}.mp3")
        os.makedirs("podcasts", exist_ok=True)
        final_mix.export(output_path, format="mp3")
        print(f"[INFO] Podcast exported to {output_path}")
    
    export_final_podcast(audio_files)

if __name__ == '__main__':
    main()
