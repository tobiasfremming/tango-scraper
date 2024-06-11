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
        


class TextExtractor:
    def __init__(self):
        self.reader: TextReader = TextReader()
        self.post_processor: PostProcessor = PostProcessor()

    def extractData(self, file: InMemoryUploadedFile) -> list[Page]:
        """Decides whether to extract text from a PDF file or an image file, and extracts the text using the appropriate method. Then the extracted text is post-processed.

        Args:
            file (InMemoryUploadedFile): the file to extract text from.

        Returns:
            list[Page]: Page: text, page number and book name.
        """
        pages: list[Page] = []
        file_extension = file.name.split(".")[-1].lower()

        match file_extension:
            case "pdf":
                print("Extracting text from PDF file")
                if self._isReadable(file):
                    pages.extend(self._extractTextPdf(file))
                else:
                    pages.extend(self._extractTextImage(file))
                    
                data = self.post_processor.page_post_processing(pages)
                return data
                    
            case "doc" | "docx":
                print("Extracting text from Word document")
                doc_reader = DocReader()
                pages = doc_reader.get_text_from_doc_or_docx(file)
                
                data = self.post_processor.page_post_processing(pages)
                return data
            
            case "png" | "jpg" | "jpeg" | "ppm" | "tiff" | "bmp":
                print("Extracting text from image file")
                pages.extend(self._extractTextImage(file))
                
                data = self.post_processor.page_post_processing(pages)
                return data
    
            case _:
                raise NotImplementedError(f"Unsupported file format: {file_extension}")

        

    def _extractTextPdf(self, file: InMemoryUploadedFile) -> list[Page]:
        """Extract the text directly from a PDF file. Entrypoint for text reader class.

        Args:
            file (InMemoryUploadedFile):

        Returns:
            list[Page]: Page: text, page number and book name.
        """
        return self.reader.read(file)

    def _extractTextImage(self, file) -> list[Page]:
        """Extract the text from an image file using optical character recognition with tesseract. Entrypoint for OCR class.
        args:
            file (InMemoryUploadedFile):
        Returns:
            list[Page]:
        """

        ocr: OCR = OCR(file)
        ocr.ocr_images(file)
        page_data = ocr.get_page_data()
        print(page_data)
        
        return page_data

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

        total_pages = self.reader.get_amount_of_pages(file)
        fast_text = ""
        ocr_text = ""
        ocr = OCR(file)

        # Look random pages and see if there is a large disparity
        for _ in range(3):  # TODO: change to 3 with log2(total_pages1)
            page_number = random.randint(0, total_pages - 1)
            fast_text += self.reader.read_page(file, page_number)
            ocr_text += ocr.ocr_page(file, page_number)

        if len(ocr_text) == 0:
            return True  # TODO: lag feilmelding
        if len(fast_text) / len(ocr_text) > 0.88:
            return True
        return False
