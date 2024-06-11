

from django.core.files.uploadedfile import InMemoryUploadedFile
from data_format import Page

class MP3TextScraper(TextScraper):
    
    def extract_text(self, file: InMemoryUploadedFile) -> list[Page]:
        """
        Extracts text from an MP3 file.
        """
        print("Extracting text from MP3 file")
        
        