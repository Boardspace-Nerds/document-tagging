from pypdf import PdfReader
from pydantic import BaseModel
from typing import Iterable, List

class DocumentTokenBatch(BaseModel):
    page_number: int 
    text: str

class DocumentParser:
    document_filepath: str
    token_batch_size: int
    
    def __init__(self, document_filepath: str, token_batch_size: int = 20):
        self.document_filepath = document_filepath  
        self.token_batch_size = token_batch_size
        self.pdf_reader = PdfReader(stream=self.document_filepath)

    def _create_token_batch(self, page_number: int, tokens: List[str]) -> DocumentTokenBatch:
        batch_text = " ".join(tokens).strip().replace('\n', ' ')
        return DocumentTokenBatch(page_number=page_number, text=batch_text)
    
    def get_token_batches(self) -> Iterable[DocumentTokenBatch]:
        for page in self.pdf_reader.pages:
            page_text = page.extract_text()
            page_number = page.page_number
            current_batch_tokens: List[str] = []

            for text_token in page_text.split(' '):
                if len(current_batch_tokens) == self.token_batch_size:
                    yield self._create_token_batch(page_number=page_number, tokens=current_batch_tokens)

                    current_batch_tokens.clear()
                    current_batch_tokens.append(text_token)
                else:
                    current_batch_tokens.append(text_token)
                
            if len(current_batch_tokens) > 0:
                yield self._create_token_batch(page_number=page_number, tokens=current_batch_tokens)


        