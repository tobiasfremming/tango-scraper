from dataclasses import dataclass


@dataclass
class Page:
    text: str
    page_num: int
    document_name: str

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "page_num": self.page_num,
            "document_name": self.document_name,
        }