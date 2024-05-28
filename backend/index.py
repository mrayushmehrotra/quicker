# #imports 
# from pytube import YouTube
# from youtube_transcript_api import YouTubeTranscriptApi
# import re 
# from pytube import YouTube



# #enter the url and extract the necessary things
# url = input("Enter the Youtube Video/Podcast: ")
# try:
#     #function to download the video 
#     def download_video(url):
#         yt = YouTube(url)
#         title = yt._title()
#         print(title)
#         #get all the stream and filter for mp4
#         mp4_stream = yt.streams.filter(file_extension='mp4').all()
#         #downlaod the highest quality
#         d_video = mp4_stream[-1]
#         # d_video.download()
#         print("video downloaded successfully")
    
#     pattern_for_yt_videoId = r"[?&]v=([^&]+)"
#     match = re.search(pattern_for_yt_videoId, url)
#     if match:
#         video_id = match.group(1)
#     else:
#         print("Please enter a valid or complete YT Video url")

#     #downloading SRT file  and extracting Subs only
#     srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
#     print(srt)
#     text_only = [item['text'] for item in srt] 
#     result = " ".join(text_only)
#     pattern_for_bracketed_text =  r"\[.*?\]" # to remove [Music] and etc. in srt file
#     cleaned_text = re.sub(pattern_for_bracketed_text, "", result)
#     cleaned_text = cleaned_text.strip() 
#     # print(cleaned_text)
# except Exception as e:
#     print("Error", e)

# imports
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import re
from moviepy.editor import VideoFileClip, concatenate_videoclips
import imageio 
imageio.plugins.ffmpeg.download()

# enter the url and extract the necessary things
url = input("Enter the Youtube Video/Podcast: ")
try:
    # function to download the video
    def download_video(url):
        yt = YouTube(url)
        title = yt.title
        print(f"Title: {title}")
        # get all the streams and filter for progressive mp4 (both video and audio)
        mp4_streams = yt.streams.filter(progressive=True, file_extension='mp4')
        # download the highest quality
        d_video = mp4_streams.order_by('resolution').desc().first()
        video_path = d_video.download()
        print("Video downloaded successfully")
        return video_path
    
    pattern_for_yt_videoId = r"[?&]v=([^&]+)"
    match = re.search(pattern_for_yt_videoId, url)
    if match:
        video_id = match.group(1)
    else:
        print("Please enter a valid or complete YT Video url")
        exit()

    # downloading SRT file and extracting subs only
    srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    filtered_srt = [item for item in srt if not re.search(r"\[.*?\]", item['text'])]

    # Download the video
    video_path = download_video(url)

    # Load the video file
    video = VideoFileClip(video_path)

    # Create a list to hold the video clips
    clips = []

    # Iterate through the filtered subtitles and create clips
    for sub in filtered_srt:
        start_time = sub['start']
        end_time = start_time + sub['duration']
        clip = video.subclip(start_time, end_time)
        clips.append(clip)

    # Concatenate all the clips
    final_clip = concatenate_videoclips(clips)

    # Save the final concatenated clip
    final_clip_path = "short_video.mp4"
    final_clip.write_videofile(final_clip_path, codec='libx264', audio_codec='aac')

    print(f"Short video created and saved as {final_clip_path}")

except Exception as e:
    print("Error", e)
