# News Podcast Maker

## Overview

This tool generates a podcast from the latest news using Python, a News API, OpenAI's Chat Completions API, TTS APIs, and various Python libraries. It retrieves news URLs, captures screenshots, extracts article text, converts content into podcast segments with two hosts, generates voiceovers, and merges everything with background music and sound effects.

## Getting Started

**Requirements:**
- Python 3.9.6
- Tesseract OCR (`brew install tesseract`)
- Dependencies (`pip install -r requirements.txt`)
    - requirements.txt includes some testing dependencies to avoid breaking functionality.
- Playwright (`playwright install`)

**Environment Setup:**
Create a `.env` file in the root directory with the following:
```
OPENAI_API_KEY=your_openai_api_key_here
NEWSAPI_API_KEY=your_newsapi_key_here
```

**Notes:**
- Required directories are auto-generated on first run
- Static sound assets are in the `public` directory

## Known Limitations

- Article extraction often fails (~30-40% fail rate per article). Playwright has limitations; Selenium could be more robust but slower.
- Extensive error handling is in place, but extraction failures can't always be recovered.
- AI-generated content may include inaccuracies.
- Depending on the number of clips, generation may take several minutes (up to ~4 minutes).
- The cost insight printed to the console at the end is only a guess and only includes audio gen costs (estimated).
- Some chat completion calls are probably unessesary, but I've found the current set of prompts and calls to give the best results.

## Credits

**Sound Effects & Music:**
- **Intro Sound:** Sound Effect by [Vlad Krotov](https://pixabay.com/users/moodmode-33139253/) from [Pixabay](https://pixabay.com/sound-effects/)
- **Outro Sound:** Sound Effect by [vynadot](https://pixabay.com/users/vynadot-36505577/) from [Pixabay](https://pixabay.com/sound-effects/)
- **Background Music:** Music by [WaveMaster](https://pixabay.com/users/wavemaster-13802185/) from [Pixabay](https://pixabay.com/)
- **Generation Wait Music:** "On & On" by Cartoon, Jéja (feat. Daniel Levi) - [NCS](https://www.youtube.com/watch?v=K4DyBUG242c)
  - *Previously used: "Space Walk" by Silent Partner (removed due to copyright)*
