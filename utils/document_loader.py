# utils/document_processor.py
import json
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def process_jsonl(file_path):
    docs = []
    with open(file_path) as f:
        for line in f:
            data = json.loads(line)
            docs.append(Document(
                page_content=data["content"],
                metadata={"source": "jsonl", "page": data.get("page", 0)}
            ))
    return docs

def process_book(book_path):
    # Use appropriate loader (PyPDF2 for PDFs, etc.)
    from langchain.document_loaders import PyPDFLoader
    loader = PyPDFLoader(book_path)
    return loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)