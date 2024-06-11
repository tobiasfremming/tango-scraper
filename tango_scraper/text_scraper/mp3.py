

import os
import speech_recognition as sr
from django.core.files.uploadedfile import InMemoryUploadedFile
from pydub.silence import split_on_silence
from pydub import AudioSegment
from data_format import Page
from io import BytesIO


class MP3TextScraper():
    
    def convertToWav(file: InMemoryUploadedFile) -> InMemoryUploadedFile:
        """
        Converts the input audio file to WAV format if necessary and returns the InMemoryUploadedFile of the WAV file.
        Args:
            file: The file to convert
        Returns:
            InMemoryUploadedFile: The converted file
        """
        file_ext = os.path.splitext(file.name)[1]
        
        if file_ext == '.wav':
            return file
        elif file_ext in ('.mp3', '.m4a', '.ogg', '.flac'):
            audio_file = AudioSegment.from_file(file, format=file_ext[1:])
            wav_io = BytesIO()
            audio_file.export(wav_io, format='wav')
            wav_io.seek(0)
            wav_file = InMemoryUploadedFile(wav_io, file.field_name, os.path.splitext(file.name)[0] + '.wav', 'audio/wav', wav_io.getbuffer().nbytes, None)
            return wav_file
        else:
            raise ValueError(f'Unsupported audio format: {file_ext}')
        
    def transcribe_audio(audio_data, language = "en-US") -> str:
        """
        Transcribes audio data to text using Google's speech recognition API.
        Args:
            file: audio_data; the audio data to transcribe
        Returns:
            str: The transcribed text
        """
        r = sr.Recognizer()
        try:
            text = r.recognize_google(audio_data, language=language)
        except sr.UnknownValueError as e:
            print("Error:", str(e))
            text = ""
        return text
    
    
    def speech_to_text(self, file: InMemoryUploadedFile) -> list[Page]:
        """
        Transcribes an audio file to text.
        Args:
            file: The file to transcribe
        Returns:
            list[Page]: The converted file
        """
        file = self.convertToWav(file)
        folder_name = "audio-chunks"
        language = "en-US" # I might have to do something that recognizes the language of the audio file
        
        audio: AudioSegment = AudioSegment.from_file(file)
        min_silence_len = 1000 # 1 second. I might have to adjust this for different sounds
        silence_thresh = -16 # I might have to adjust this for different sounds
        keep_silence = 1000 # 1 second. I might have to adjust this for different sounds
        audio_chunks: list[AudioSegment] = split_on_silence(audio, min_silence_len, silence_thresh, keep_silence)[0]
        
        data: list[Page]= []
        
        for index, chunk in enumerate(audio_chunks):
            chunk_filename = os.path.join(folder_name, f"chunk{index}.wav")
            chunk.export(format="wav")
            
            with sr.AudioFile(chunk_filename) as source: # unsure if i should use chunck filename or chunk
                audio_data = sr.Recognizer().record(source)
                text = self.transcribe_audio(audio_data, language)
                
                data.append(Page(text, index + 1, file.name))
                
        return data

        
   
            
           
            
            
            

            
            
            
        
        
        
        