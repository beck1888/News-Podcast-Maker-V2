from openai import OpenAI
from pathlib import Path
import uuid

"""
Generate audio using the OpenAI TTS API and speaks it out loud.

Parameters:
text (str): The text to be spoken.
voice (str): The name of the voice to use. Defaults to "onyx".
wait_for_speech_to_stop (bool): Whether to wait for the speech to stop. Defaults to True.
clean_up (bool): Whether to clean up the temporary audio file. Defaults to True.

Returns:
str: The path to the temporary audio file (if applicable).
"""

def gen_speech(text: str, api_key: str, voice="coral") -> str:
    # Initialize the OpenAI API client
    client = OpenAI(api_key=api_key)

    # Structure the request
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )

    # Save to 'tmp' in the project root (where main.py is run from)
    tmp_dir = Path.cwd() / "tmp"
    tmp_dir.mkdir(exist_ok=True)

    speech_file_path = tmp_dir / f"{uuid.uuid4()}.mp3"
    response.write_to_file(speech_file_path)

    return str(speech_file_path)
