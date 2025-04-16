# document_loader.py
import json
import logging
from pathlib import Path
from typing import List, Optional

from langchain.schema import Document
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentLoader:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            add_start_index=True
        )

    def load_jsonl(self, file_path: str) -> List[Document]:
        """Load and process JSONL file with mental health Q&A pairs"""
        docs = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    try:
                        data = json.loads(line)
                        
                        # Handle both original and improved formats
                        if "instruction" in data and "output" in data:
                            content = f"Question: {data['instruction']}\nAnswer: {data['output']}"
                            metadata = {
                                "source": "jsonl",
                                "line_number": i,
                                "type": "qa_pair"
                            }
                        elif "question" in data and "answer" in data:
                            content = f"Question: {data['question']}\nAnswer: {data['answer']}"
                            metadata = {
                                "source": "jsonl",
                                "line_number": i,
                                "type": "qa_pair",
                                **data.get("metadata", {})
                            }
                        else:
                            logger.warning(f"Skipping malformed entry at line {i}")
                            continue
                            
                        docs.append(Document(
                            page_content=content,
                            metadata=metadata
                        ))
                    except json.JSONDecodeError as e:
                        logger.error(f"Error parsing line {i}: {e}")
                        
            logger.info(f"Loaded {len(docs)} documents from {file_path}")
            return docs
            
        except Exception as e:
            logger.error(f"Failed to load JSONL file {file_path}: {e}")
            raise

    def load_pdf(self, file_path: str) -> List[Document]:
        """Load and process PDF file"""
        try:
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            
            # Add consistent metadata
            for doc in docs:
                doc.metadata.update({
                    "source": Path(file_path).name,
                    "type": "book_page"
                })
                
            logger.info(f"Loaded {len(docs)} pages from {file_path}")
            return docs
            
        except Exception as e:
            logger.error(f"Failed to load PDF file {file_path}: {e}")
            raise

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        try:
            chunked_docs = self.text_splitter.split_documents(documents)
            logger.info(f"Split {len(documents)} documents into {len(chunked_docs)} chunks")
            return chunked_docs
        except Exception as e:
            logger.error(f"Failed to chunk documents: {e}")
            raise


# Example usage:
if __name__ == "__main__":
    loader = DocumentLoader()
    
    # Test loading
    jsonl_docs = loader.load_jsonl("data/mental_health_resources/mental_health_dataset.jsonl")
    pdf_docs = loader.load_pdf("data/mental_health_resources/sample_book.pdf")
    
    # Test chunking
    chunked_docs = loader.chunk_documents(jsonl_docs + pdf_docs)
    print(f"Total chunks created: {len(chunked_docs)}")