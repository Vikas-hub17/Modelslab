import yt_dlp
from moviepy.editor import VideoFileClip
import os

def download_youtube_video(url):
    """
    Downloads the audio of a YouTube video using yt-dlp and saves it in the current directory.
    Returns the path to the downloaded file.
    """
    # Define options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloaded_video.%(ext)s',  # Temporary file name
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    
    # Download the audio file
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # After downloading, locate the file
        downloaded_file = 'downloaded_video.wav'
        if os.path.exists(downloaded_file):
            return downloaded_file
        else:
            raise FileNotFoundError("Downloaded audio file was not found.")
        
    except Exception as e:
        print(f"Error downloading video: {e}")
        raise e