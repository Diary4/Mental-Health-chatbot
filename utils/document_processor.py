# utils/document_processor.py
import json
import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    TextLoader,
    JSONLoader
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MentalHealthDocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=150,
            separators=["\n\n", "\n", r"(?<=\. )", r"(?<=\! )", r"(?<=\? )", ";", ":", ",", " ", ""],
            length_function=len
        )
        self.supported_extensions = {
            '.jsonl': self._process_jsonl,
            '.txt': self._process_txt,
            '.pdf': self._process_pdf,
            '.csv': self._process_csv,
            '.json': self._process_json
        }

    def process_file(self, file_path: str) -> List[Document]:
        """Process a single file based on its extension"""
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return []

        ext = file_path.suffix.lower()
        if ext in self.supported_extensions:
            try:
                return self.supported_extensions[ext](file_path)
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                return []
        else:
            logger.warning(f"Unsupported file type: {ext}")
            return []

    def _process_jsonl(self, file_path: Path) -> List[Document]:
        """Specialized processor for mental health Q&A JSONL files"""
        docs = []
        try:
            # Use LangChain's JSONLoader with custom jq schema
            loader = JSONLoader(
                file_path=str(file_path),
                jq_schema=".[] | {content: (.instruction + \" \" + .output), metadata: {source: input_filename, type: \"qa_pair\"}}",
                text_content=False
            )
            docs = loader.load()
            logger.info(f"Loaded {len(docs)} Q&A pairs from {file_path.name}")
        except Exception as e:
            logger.error(f"JSONL loading failed, falling back to manual parsing: {e}")
            # Fallback to manual processing
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        data = json.loads(line)
                        content = ""
                        metadata = {
                            "source": file_path.name,
                            "line": line_num,
                            "type": "qa_pair"
                        }

                        # Handle multiple possible structures
                        if "instruction" in data and "output" in data:
                            content = f"Q: {data['instruction']}\nA: {data['output']}"
                        elif "question" in data and "answer" in data:
                            content = f"Q: {data['question']}\nA: {data['answer']}"
                        elif "content" in data:
                            content = data["content"]
                        
                        if content:
                            # Add additional metadata fields
                            for field in ["topic", "severity", "tags"]:
                                if field in data:
                                    metadata[field] = data[field]
                            docs.append(Document(page_content=content, metadata=metadata))
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON at line {line_num} in {file_path}")
        
        return docs

    def _process_pdf(self, file_path: Path) -> List[Document]:
        """Process PDF files with mental health content"""
        try:
            loader = PyPDFLoader(str(file_path))
            docs = loader.load()
            for doc in docs:
                doc.metadata.update({
                    "source": file_path.name,
                    "type": "book_page",
                    "chunk_type": "pdf_text"
                })
            logger.info(f"Loaded {len(docs)} pages from {file_path.name}")
            return docs
        except Exception as e:
            logger.error(f"Failed to load PDF {file_path.name}: {e}")
            return []

    def _process_txt(self, file_path: Path) -> List[Document]:
        """Process text files with mental health articles"""
        try:
            loader = TextLoader(str(file_path))
            docs = loader.load()
            for doc in docs:
                doc.metadata.update({
                    "source": file_path.name,
                    "type": "article",
                    "chunk_type": "plain_text"
                })
            logger.info(f"Loaded text file: {file_path.name}")
            return docs
        except Exception as e:
            logger.error(f"Failed to load text file {file_path.name}: {e}")
            return []

    def _process_csv(self, file_path: Path) -> List[Document]:
        """Process CSV files with mental health resources"""
        try:
            loader = CSVLoader(
                file_path=str(file_path),
                source_column="source",
                metadata_columns=["category", "tags", "url"]
            )
            docs = loader.load()
            for doc in docs:
                doc.metadata.update({
                    "type": "structured_data",
                    "chunk_type": "csv_row"
                })
            logger.info(f"Loaded {len(docs)} rows from {file_path.name}")
            return docs
        except Exception as e:
            logger.error(f"Failed to load CSV {file_path.name}: {e}")
            return []

    def _process_json(self, file_path: Path) -> List[Document]:
        """Process regular JSON files"""
        try:
            loader = JSONLoader(
                file_path=str(file_path),
                jq_schema=".[]",
                text_content=False
            )
            docs = loader.load()
            for doc in docs:
                doc.metadata.update({
                    "source": file_path.name,
                    "type": "json_data"
                })
            logger.info(f"Loaded JSON data from {file_path.name}")
            return docs
        except Exception as e:
            logger.error(f"Failed to load JSON {file_path.name}: {e}")
            return []

    def process_directory(self, data_dir: str) -> List[Document]:
        """Process all supported files in a directory"""
        docs = []
        data_path = Path(data_dir)
        
        if not data_path.exists():
            logger.error(f"Directory not found: {data_dir}")
            return docs

        for file_path in data_path.iterdir():
            if file_path.is_file():
                docs.extend(self.process_file(file_path))
        
        logger.info(f"Loaded {len(docs)} documents total from {data_dir}")
        return docs

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks with mental health context preservation"""
        if not documents:
            return []
            
        try:
            chunks = self.text_splitter.split_documents(documents)
            # Add chunk-specific metadata
            for i, chunk in enumerate(chunks):
                chunk.metadata["chunk_id"] = i
                chunk.metadata["chunk_size"] = len(chunk.page_content)
            
            logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")
            return chunks
        except Exception as e:
            logger.error(f"Failed to chunk documents: {e}")
            return []
            
def load_all_documents(data_dir: str) -> List[Document]:
    processor = MentalHealthDocumentProcessor()
    return processor.process_directory(data_dir)

def split_documents(documents: List[Document]) -> List[Document]:
    processor = MentalHealthDocumentProcessor()
    return processor.chunk_documents(documents)


# Example usage
if __name__ == "__main__":
    processor = MentalHealthDocumentProcessor()
    
    # Test processing
    test_dir = "data/mental_health_resources"
    documents = processor.process_directory(test_dir)
    
    if documents:
        chunks = processor.chunk_documents(documents)
        if chunks:
            print("\nSample chunk:")
            print(f"Content: {chunks[0].page_content[:200]}...")
            print(f"Metadata: {chunks[0].metadata}")
            print(f"\nTotal chunks created: {len(chunks)}")