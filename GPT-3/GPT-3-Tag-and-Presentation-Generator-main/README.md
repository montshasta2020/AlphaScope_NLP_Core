# GPT-3 Hackathon - Team GPTFR33
The official repo of team GPTFR33 for TUM.ai's GPT-3 Hackathon. The goal of this project is to use GPT-3 to generate a title, tags, short summaries and instructions based on a transcription of an educational video. Furthermore, a Google Slides presentation can be generated from the video transcription. This functions enhance the user experience on the Zesavi platform.

## Description 
Repository contains following functionalities:

- Generate tags from text script 

- Generate short summary from text script

- Generate title from text script 

- Generate instructions from text script 

Functions are merged in `open_ai_utils.py`.

The folder python-getting-started contains a complete django server (with some specific heroku specific files which are not required for the code to work) that handles the conversion of transcripts to presentations as well as the authentication to google. The button in `presentation_generation/hello/templates/slideshow-api-sender.html` can be used to redirect a user to this server at `/slideshow-api/` with the required POST data. The user then grants access to google. The presentation is generated and the user is redirected.

The following environment variables have to be set:
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `FLATICON_KEY`
- `UNSPLASH_KEY`
- `OPENAI_KEY`

## Team Members

Adam Misik

Jonas Jürß

Pierre Toussing

## References 

Open AI API Examples: https://beta.openai.com/examples
