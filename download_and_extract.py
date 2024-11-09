from pytube import YouTube
from moviepy.editor import VideoFileClip

def download_youtube_video(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    output_path = stream.download()
    return output_path

def extract_audio(video_path):
    clip = VideoFileClip(video_path)
    audio_path = video_path.replace(".mp4", ".wav")
    clip.audio.write_audiofile(audio_path)
    clip.close()
    return audio_path
