
from django.core.files.uploadedfile import InMemoryUploadedFile
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os


class VideoScraper:
    
    def extract_audio_file_from_youtube(self, url: str) -> InMemoryUploadedFile:
        """Download the audio file from the given url.
        Args:
            url (str): the url of the video.
        Returns:
            InMemoryUploadedFile: the audio file.
        """
        filename = "yt_file_audio_extraction"

        # Download the video
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download()

        # Extract the audio
        video = VideoFileClip(filename+".mp4")
        audio = video.audio
        audio.write_audiofile(filename+".mp3")

        # Delete the downloaded video file
        os.remove('filename.mp4')
                
        return InMemoryUploadedFile(open("audio.mp3", "rb"), None, "audio.mp3", "audio/mp3", os.path.getsize("audio.mp3"), None)
        