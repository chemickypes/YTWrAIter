from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from cat.mad_hatter.decorators import tool


def private_get_transcription(video_id: str, language="it"):
    data = YouTubeTranscriptApi.get_transcript(video_id, languages=[language, "en"])
    transcription = []
    for item in data:
        transcription.append(item['text'])

    return {'video_id': video_id, "language": language, "text": "\n".join(transcription)}


@tool
def get_transcription(tool_input, cat):
    """Useful to get transcription of a Youtube Video. This tool get a video id and returns the transcription.
    The inputs are two values separated with a minus: the first one is video id and from a youtube url is the query parameter v;
    the second one is language in iso format for get the transcription. Example input: "HDJZrp0Hfiw-it".
    Use when the user says something like: 'give me the transcription of the video https://www.youtube.com/watch?v=HDJZrp0Hfiw using italian'"""

    params = tool_input.split('-')
    transcription = private_get_transcription(params[0], params[1])
    return transcription['text']
