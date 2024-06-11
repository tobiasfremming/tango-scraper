import random
from django.core.files.uploadedfile import InMemoryUploadedFile

from data_format import Page
from text_scraper.doc_reader import DocReader
from text_scraper.text_reader import TextReader
from text_scraper.post_processing import PostProcessor
from text_scraper.ocr import OCR
from abc import ABC, abstractmethod
from text_scraper.strategy import StrategyFactory, Strategy



class Scraper:
    
    def extract(self, file: InMemoryUploadedFile) -> list[Page]:
        """Decides how to extract, and extracts the text using the appropriate method. Then the extracted text is post-processed.

        Args:
            file (InMemoryUploadedFile): the file to extract text from.

        Returns:
            list[Page]: Page: text, page number and book name.
        """
        pages: list[Page] = []
        file_extension = file.name.split(".")[-1].lower()
        
        strategy: Strategy = StrategyFactory().get_strategy(file_extension)
        
        


















