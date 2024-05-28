from youtube_transcript_api import YouTubeTranscriptApi

srt = YouTubeTranscriptApi.get_transcript("SW14tOda_kI")

text_only = [item['text'] for item in srt] 

result = " ".join(text_only)

print(result)