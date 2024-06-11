



import random
from django.core.files.uploadedfile import InMemoryUploadedFile

from data_format import Page
from text_scraper.doc_reader import DocReader
from text_scraper.text_reader import TextReader
from text_scraper.post_processing import PostProcessor
from text_scraper.ocr import OCR
from text_scraper.soundScraper import SoundScraper
from abc import ABC, abstractmethod

class Strategy(ABC):
    
    @abstractmethod
    def execute(self, file: InMemoryUploadedFile) -> list[Page]:
        """executes the strategy to extract text from the file.
        Args:
            file (InMemoryUploadedFile): the file to extract text from.
        Returns:
            list[Page]: the extracted text from the file.
        """
        pass
    
    
class ReadPDFStrategy(Strategy):
    
    def execute(self, file: InMemoryUploadedFile) -> list[Page]:
        # TODO: implement the correct logic
        print("Extracting text from PDF file")
        reader: TextReader = TextReader()
        post_processor: PostProcessor = PostProcessor()
        pages: list[Page] = []
        
        pages.extend(reader.read(file))
        data = post_processor.page_post_processing(pages)
        
        return data
    
    
class OCRStrategy(Strategy):
    def execute(self, file: InMemoryUploadedFile) -> list[Page]:
        # TODO: implement the correct logic
        print("Extracting text from image file")
        
        return []
    
class ReadDocStrategy(Strategy):
    def execute(self, file: InMemoryUploadedFile) -> list[Page]:
        # TODO: implement the correct logic
        print("Extracting text from Word document")
        return []
        
class SoundStrategy(Strategy):
    def execute(self, file: InMemoryUploadedFile) -> list[Page]:
        
        print("Extracting text from Sound file")
        return SoundScraper.speech_to_text(file)
        
class EpubStrategy(Strategy):
    def execute(self, file: InMemoryUploadedFile) -> list[Page]:
        # TODO: implement the correct logic
        print("Extracting text from EPUB file")
        return []
        
class URLStrategy(Strategy):
    def execute(self, file: InMemoryUploadedFile) -> list[Page]:
        # TODO: implement the correct logic
        print("Extracting text from URL")
        return []
    
    
class StrategyFactory:
    def get_strategy(self, file: InMemoryUploadedFile) -> Strategy:
        """Choose the correct strategy based on the file extension and readability of the file.
        Args:
            file (InMemoryUploadedFile): The file to extract text from.
        Returns:
            Strategy: The strategy to use for extracting text from the file. 
        """
        
        file_extension = file.name.split(".")[-1].lower()
        match file_extension:
            case "pdf":
                if self._isReadable(file):
                    return ReadPDFStrategy()
                return OCRStrategy()
            case "doc" | "docx":
                return ReadDocStrategy()
            case "mp3"| "wav" | "flac" | "ogg" | "m4a":
                return SoundStrategy()
            case "epub":
                return EpubStrategy()
            case "url":
                return URLStrategy()
            case _:
                return OCRStrategy()
            
            
    def _isReadable(self, file: InMemoryUploadedFile) -> bool:
        """
        Checks if a PDF file is easily readable by attempting to extract text directly from it.

        This method does not guarantee OCR accuracy but checks if the PDF contains selectable text,
        which is a good indicator of the document's readability without needing image conversion.

        Args:
            file: The PDF file to check.

        Returns:
            True if the file is easily readable (contains a significant amount of selectable text),
            False otherwise.
        """

        total_pages = TextReader.get_amount_of_pages(file)
        fast_text = ""
        ocr_text = ""
        ocr = OCR(file)

        # Look random pages and see if there is a large disparity
        for _ in range(3):  # TODO: change to 3 with log2(total_pages1)
            page_number = random.randint(0, total_pages - 1)
            fast_text += TextReader.read_page(file, page_number)
            ocr_text += ocr.ocr_page(file, page_number)

        if len(ocr_text) == 0:
            return True  # TODO: lag feilmelding
        if len(fast_text) / len(ocr_text) > 0.88:
            return True
        return False
        