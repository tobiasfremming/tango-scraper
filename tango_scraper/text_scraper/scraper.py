from django.core.files.uploadedfile import InMemoryUploadedFile
from data_format import Page
from post_processing import PostProcessor
from strategy import StrategyFactory, Strategy



class Scraper:
    
    def extract(self, file: InMemoryUploadedFile, post_process: bool) -> list[Page]:
        """Decides how to extract, and extracts the text using the appropriate method. Then the extracted text is post-processed.

        Args:
            file (InMemoryUploadedFile): the file to extract text from.

        Returns:
            list[Page]: Page: text, page number and book name.
        """
        pages: list[Page] = []
        file_extension = file.name.split(".")[-1].lower()
        
        strategy: Strategy = StrategyFactory().get_strategy(file_extension)
        pages.extend(strategy.execute(file))
        # delete possible temp file after use
        if post_process:
            pages = PostProcessor().page_post_processing(pages)
            
        return pages  
    
    def extract(self, file: InMemoryUploadedFile) -> list[Page]:
        """Decides how to extract, and extracts the text using the appropriate method. 

        Args:
            file (InMemoryUploadedFile): the file to extract text from.

        Returns:
            list[Page]: Page: text, page number and book name.
        """  
        return self.extract(file, False)
        
        







if __name__ == '__main__':

    print("hei")

    url = "https://www.youtube.com/watch?v=6JYIGclVQdw"
    print("hei2")
    file = InMemoryUploadedFile(url, None, None, None, None, None)
    print("hei3")
    scraper = Scraper()
    print("hei4")
    text: list[Page] = scraper.extract(file)
    print("hei5")
    print(text[0].text)
    










