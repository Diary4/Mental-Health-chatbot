# utils/index_builder.py
import os
import logging
from pathlib import Path
from typing import Optional

from utils.document_processor import MentalHealthDocumentProcessor
from services.retrieval_service import MentalHealthRetrievalService as RetrievalService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_mental_health_index(data_dir: str = "data/mental_health_resources") -> bool:
    """
    Build and update the vector index from mental health resources
    
    Args:
        data_dir: Directory containing mental health resources
        
    Returns:
        bool: True if indexing succeeded, False otherwise
    """
    try:
        logger.info(f"Building index from {data_dir}...")
        
        processor = MentalHealthDocumentProcessor()
        retrieval_service = RetrievalService()
        
        documents = processor.process_directory(data_dir)
        if not documents:
            logger.error("No documents found in directory")
            return False
            
        logger.info(f"Processing {len(documents)} documents...")
        
        chunks = processor.chunk_documents(documents)
        if not chunks:
            logger.error("No chunks created from documents")
            return False
            
        logger.info(f"Created {len(chunks)} chunks for indexing")
        
        success = retrieval_service.index_documents(chunks)
        if success:
            logger.info("Index built successfully")
        else:
            logger.error("Failed to build index")
            
        return success
        
    except Exception as e:
        logger.error(f"Error building index: {e}")
        return False


def clear_and_rebuild_index(data_dir: str = "data/mental_health_resources") -> bool:
    """
    Completely rebuild the index from scratch
    
    Args:
        data_dir: Directory containing source files
        
    Returns:
        bool: True if successful rebuild
    """
    try:
        retrieval_service = RetrievalService()
        if not retrieval_service.clear_index():
            logger.error("Failed to clear existing index")
            return False
            
        return build_mental_health_index(data_dir)
    except Exception as e:
        logger.error(f"Error during rebuild: {e}")
        return False


if __name__ == "__main__":
    build_mental_health_index()
    