#imports 
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import re 

#enter the url and extract the necessary things
url = input("Enter the Youtube Video/Podcast")
pattern_for_yt_videoId = r"[?&]v=([^&]+)"
match = re.search(pattern_for_yt_videoId, url)
if match:
    video_id = match.group(1)
else:
    print("Please enter a valid or complete YT Video url")

#downloading SRT file  and extracting Subs only
srt = YouTubeTranscriptApi.get_transcript(video_id)
text_only = [item['text'] for item in srt] 
result = " ".join(text_only)
pattern_for_bracketed_text =  r"\[.*?\]" # to remove [Music] and etc. in srt file
cleaned_text = re.sub(pattern_for_bracketed_text, "", result)
cleaned_text = cleaned_text.strip() 
print(cleaned_text)