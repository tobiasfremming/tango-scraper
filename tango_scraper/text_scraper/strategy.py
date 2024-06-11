



import random
from django.core.files.uploadedfile import InMemoryUploadedFile

from data_format import Page
from text_scraper.doc_reader import DocReader
from text_scraper.text_reader import TextReader
from text_scraper.post_processing import PostProcessor
from text_scraper.ocr import OCR
from abc import ABC, abstractmethod

class Strategy(ABC):
    
    @abstractmethod
    def __call__(self, file: InMemoryUploadedFile) -> list[Page]:
        pass
    
    
class ReadPDFStrategy(Strategy):
    
    def __call__(self, file: InMemoryUploadedFile) -> list[Page]:
        # TODO: implement the correct logic
        print("Extracting text from PDF file")
        reader: TextReader = TextReader()
        post_processor: PostProcessor = PostProcessor()
        pages: list[Page] = []
        
        pages.extend(reader.read(file))
        data = post_processor.page_post_processing(pages)
        return data
    
    
class OCRStrategy(Strategy):
    def __call__(self, file: InMemoryUploadedFile) -> list[Page]:
        # TODO: implement the correct logic
        print("Extracting text from image file")
        
        return []
    
class ReadDocStrategy(Strategy):
    def __call__(self, file: InMemoryUploadedFile) -> list[Page]:
        # TODO: implement the correct logic
        print("Extracting text from Word document")
        return []
        
class Mp3Strategy(Strategy):
    def __call__(self, file: InMemoryUploadedFile) -> list[Page]:
        # TODO: implement the correct logic
        print("Extracting text from MP3 file")
        return []
        
class EpubStrategy(Strategy):
    def __call__(self, file: InMemoryUploadedFile) -> list[Page]:
        # TODO: implement the correct logic
        print("Extracting text from EPUB file")
        return []
        
class URLStrategy(Strategy):
    def __call__(self, file: InMemoryUploadedFile) -> list[Page]:
        # TODO: implement the correct logic
        print("Extracting text from URL")
        return []
    
    
class StrategyFactory:
    def get_strategy(self, file: InMemoryUploadedFile) -> Strategy:
        file_extension = file.name.split(".")[-1].lower()
        match file_extension:
            case "pdf":
                if self._isReadable(file):
                    return ReadPDFStrategy()
                return OCRStrategy()
            case "doc" | "docx":
                return ReadDocStrategy()
            case "mp3":
                return Mp3Strategy()
            case "epub":
                return EpubStrategy()
            case "url":
                return URLStrategy()
            case _:
                return OCRStrategy()
        