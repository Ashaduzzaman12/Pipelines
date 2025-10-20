
# Imports
import whisper
import yt_dlp
import os
from glob import glob

# Function to download YouTube audio
def download_youtube_audio(url, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title', None)

    # Find the downloaded .mp3 file
    files = glob(os.path.join(output_dir, '*.mp3'))
    if not files:
        raise FileNotFoundError("MP3 file not found after download.")
    return files[0]

# Function to transcribe (modified to force English)
def transcribe_audio_whisper(audio_path):
    model = whisper.load_model("base")  # Choose: tiny, base, small, medium, large
    result = model.transcribe(audio_path, language="en")  # Force English
    return result["text"]

# Replace with your YouTube video URL
video_url = "https://youtu.be/2KAlS6u9dik?si=edXhjI5FIV56DkZh"  # <-- Replace with your actual link

# Run the full pipeline
audio_path = download_youtube_audio(video_url)
print(f"Downloaded audio: {audio_path}")

transcription = transcribe_audio_whisper(audio_path)
print("------ TRANSCRIPT ------")
print(transcription)
