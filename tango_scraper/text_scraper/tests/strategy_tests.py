

import unittest
from django.core.files.uploadedfile import InMemoryUploadedFile

from text_scraper.text_extractor import Strategy, ReadPDFStrategy, OCRStrategy, ReadDocStrategy, Mp3Strategy, EpubStrategy, URLStrategy

class StrategyTest(unittest.TestCase):
    
    def test_ocr_strategy(self):
        strategy = OCRStrategy()
        self.assertEqual(strategy(InMemoryUploadedFile), [])
        
    def test_read_pdf_strategy(self):
        strategy = ReadPDFStrategy()
        self.assertEqual(strategy(InMemoryUploadedFile), [])

    def test_read_doc_strategy(self):
        strategy = ReadDocStrategy()
        self.assertEqual(strategy(InMemoryUploadedFile), [])
        
    def test_mp3_strategy(self):
        strategy = Mp3Strategy()
        self.assertEqual(strategy(InMemoryUploadedFile), [])
        
    def test_epub_strategy(self):
        strategy = EpubStrategy()
        self.assertEqual(strategy(InMemoryUploadedFile), [])
        
        
    def test_url_strategy(self):
        strategy = URLStrategy()
        self.assertEqual(strategy(InMemoryUploadedFile), [])
        
if __name__ == '__main__':
    unittest.main()
    
    
    

















