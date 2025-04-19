# services/retrieval_service.py
import os
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MentalHealthRetrievalService:
    def __init__(
        self,
        vector_store_path: str = "data/vector_store",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        device: str = "cuda" if os.environ.get("USE_CUDA", "0") == "1" else "cpu"
    ):
        """
        Enhanced retrieval service for mental health chatbot
        
        Args:
            vector_store_path: Directory to store/load vector index
            embedding_model: Name of HuggingFace embedding model
            device: Computation device ('cuda' or 'cpu')
        """
        self.vector_store_path = Path(vector_store_path)
        self.embedding_model = embedding_model
        self.device = device
        
        # Initialize components
        self.embeddings = self._initialize_embeddings()
        self.vector_store = self._initialize_vector_store()
        
    def _initialize_embeddings(self) -> Embeddings:
        """Initialize embedding model with proper configuration"""
        return HuggingFaceEmbeddings(
            model_name=self.embedding_model,
            model_kwargs={"device": self.device},
            encode_kwargs={"normalize_embeddings": True}  # Better for similarity
        )
    
    def _initialize_vector_store(self) -> Optional[VectorStore]:
        """Load existing or create new vector store"""
        try:
            if self._vector_store_exists():
                return self._load_existing_store()
            return self._create_new_store()
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            return None
            
    def _vector_store_exists(self) -> bool:
        """Check if vector store files exist"""
        required_files = ["index.faiss", "index.pkl"]
        return all((self.vector_store_path / f).exists() for f in required_files)
    
    def _load_existing_store(self) -> VectorStore:
        """Load existing FAISS index"""
        logger.info(f"Loading vector store from {self.vector_store_path}")
        return FAISS.load_local(
            folder_path=str(self.vector_store_path),
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True  # Required for newer FAISS versions
        )
    
    def _create_new_store(self) -> VectorStore:
        """Create empty vector store"""
        logger.info("Creating new vector store")
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
        return FAISS.from_documents(
            documents=[Document(
                page_content="Mental health support placeholder",
                metadata={"source": "system", "type": "placeholder"}
            )],
            embedding=self.embeddings
        )
    
    def index_documents(self, documents: List[Document]) -> bool:
        """
        Index documents with enhanced error handling and progress tracking
        
        Args:
            documents: List of documents to index
            
        Returns:
            bool: True if indexing succeeded
        """
        if not documents:
            logger.warning("No documents provided for indexing")
            return False
            
        try:
            # Add documents in batches to avoid memory issues
            batch_size = 100
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                self.vector_store.add_documents(batch)
                logger.info(f"Indexed batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")
            
            self._save_vector_store()
            logger.info(f"Successfully indexed {len(documents)} documents")
            return True
            
        except Exception as e:
            logger.error(f"Failed to index documents: {e}")
            return False
    
    def _save_vector_store(self) -> None:
        """Save vector store with error handling"""
        try:
            self.vector_store.save_local(str(self.vector_store_path))
            logger.info("Vector store saved successfully")
        except Exception as e:
            logger.error(f"Failed to save vector store: {e}")
    
    def retrieve(
        self,
        query: str,
        k: int = 3,
        score_threshold: float = 0.5,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Enhanced retrieval with similarity scoring and filtering
        
        Args:
            query: Search query
            k: Number of results to return
            score_threshold: Minimum similarity score (0-1)
            filter: Metadata filters (e.g., {"type": "qa_pair"})
            
        Returns:
            List of relevant documents
        """
        if not self.vector_store:
            logger.error("Vector store not initialized")
            return []
            
        try:
            # Use similarity search with score
            docs_and_scores = self.vector_store.similarity_search_with_score(
                query,
                k=k,
                filter=filter
            )
            
            # Filter by score threshold and unpack
            return [
                doc for doc, score in docs_and_scores
                if score >= score_threshold
            ]
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            return []
    
    def get_context_for_query(
        self,
        query: str,
        k: int = 3,
        include_sources: bool = True,
        format_for_model: bool = True
    ) -> str:
        """
        Generate formatted context for LLM with source attribution
        
        Args:
            query: User query
            k: Number of documents to include
            include_sources: Whether to include source metadata
            format_for_model: Format for LLM consumption
            
        Returns:
            Formatted context string
        """
        docs = self.retrieve(query, k=k)
        if not docs:
            return ""
            
        context_parts = []
        for doc in docs:
            content = doc.page_content
            
            if format_for_model:
                # Clean content for LLM input
                content = content.replace("\n", " ").strip()
                
            if include_sources:
                source = doc.metadata.get("source", "unknown")
                doc_type = doc.metadata.get("type", "document")
                
                if format_for_model:
                    prefix = f"[Source: {source} | Type: {doc_type}]"
                    content = f"{prefix}\n{content}"
                else:
                    content = f"From {source} ({doc_type}):\n{content}"
            
            context_parts.append(content)
        
        return "\n\n".join(context_parts)
    
    def clear_index(self) -> bool:
        """Clear the vector store index"""
        try:
            self.vector_store = self._create_new_store()
            self._save_vector_store()
            logger.info("Vector store cleared")
            return True
        except Exception as e:
            logger.error(f"Failed to clear index: {e}")
            return False
        

    def get_emotional_context(self, query: str, k: int = 2) -> str:
        """Retrieve emotionally relevant context"""
        docs = self.retrieve(query, k=k, score_threshold=0.65)
        if not docs:
            return ""
    
        # Prioritize emotional support content
        emotional_keywords = ["feel", "cope", "support", "manage", "help"]
        emotional_docs = [
            doc for doc in docs 
            if any(kw in doc.page_content.lower() for kw in emotional_keywords)
        ]
        return "\n".join(doc.page_content for doc in emotional_docs[:k])

    def is_mental_health_query(self, text: str) -> bool:
        """Classify if query requires mental health response"""
        mental_health_keywords = [
            "feel", "anxious", "depress", "stress", 
            "worthless", "therapy", "counsel"
        ]
        return any(kw in text.lower() for kw in mental_health_keywords)


# Example usage
if __name__ == "__main__":
    # Initialize service
    retrieval = MentalHealthRetrievalService()
    
    # Test retrieval
    test_query = "How to deal with feelings of worthlessness?"
    context = retrieval.get_context_for_query(test_query)
    print(f"Retrieved context:\n{context}")