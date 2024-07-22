from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from cat.mad_hatter.decorators import tool


def private_get_transcription(video_id: str, language="it"):
    try:
        data = YouTubeTranscriptApi.get_transcript(video_id, languages=[language, "en"])
        transcription = []
        for item in data: 
            transcription.append(item['text'])

        return {'video_id': video_id, "language": language, "text": " ".join(transcription)}
    except NoTranscriptFound:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_manually_created_transcript([])

            if not transcript:
                transcript = transcript_list.find_generated_transcript([])
                if transcript:
                    print(f"Restituisco la trascrizione in {transcript.language_code}")
                    data = transcript.fetch()
                    trn = []
                    for item in data:
                        trn.append(item['text'])

                    return {'video_id': video_id, "language": language, "text": " ".join(trn)}
                else:
                    print("Nessuna trascrizione disponibile.")
                    return {'video_id': video_id, "language": language,
                            "text": "Maybe we didn't find any transcription"}
        except Exception as e:
            return {'video_id': video_id, "language": language, "text": "Maybe we didn't find any transcription"}


@tool(return_direct=True,
      examples=["give me the transcription of the video https://www.youtube.com/watch?v=HDJZrp0Hfiw using italian",
                "I have this video https://www.youtube.com/watch?v=HDJZrp0Hfiw give me the transcription in italian"])
def get_transcription(tool_input, cat):
    """Useful to obtain the transcription of a YouTube video. 
    You have to use this tool get_transcription when you get something like the following sentences:
        - When the user requests: "Give me the transcription of the video https://www.youtube.com/watch?v=HDJZrp0Hfiw in Italian"
        - If someone asks: "Can you provide the English subtitles for the YouTube video with ID dQw4w9WgXcQ?"
        - When a query like this is received: "I need the Korean transcript of the Gangnam Style video"
    This tool takes a video ID and language code as input and returns the corresponding transcription.


    The Input format will be:
    - Two values separated by a hyphen (-):
    1. Video ID: Found in the 'v' query parameter of a YouTube URL the user has passed to you
    2. Language code: ISO 639-1 format (e.g., 'en' for English, 'it' for Italian)

    If the user does not send the language, please use the language after the "input" in the following of this message

    there are some Example inputs:
    - "HDJZrp0Hfiw-it" (Italian transcription)
    - "dQw4w9WgXcQ-en" (English transcription)
    - "9bZkp7q19f0-ko" (Korean transcription)

    Additional features:
    - Supports multiple languages for transcription
    - Can handle both short-form (e.g., youtu.be/abcd1234) and long-form (e.g., youtube.com/watch?v=abcd1234) YouTube URLs
    - Automatically detects and extracts the video ID from full URLs

Note: This tool requires a valid YouTube video ID and a supported language code to function correctly. It may not work for private videos, live streams, or content with disabled transcription features."""
    params = tool_input.split('-')
    transcription = private_get_transcription(params[0], params[1])
    return transcription['text']


