# services/retrieval_service.py
import os
import json
import torch
from datasets import load_dataset
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List, Optional

class MentalHealthRetrievalService:
    def __init__(self, vector_store_path: str = "vector_store"):
        self.vector_store_path = vector_store_path
        os.makedirs(vector_store_path, exist_ok=True)
        
        # Initialize with all-MiniLM-L6-v2 embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"}
        )
        
        # Load or create vector store
        self.vector_store = self._init_vector_store()

    def _init_vector_store(self):
        """Initialize FAISS vector store"""
        # Check if vector store exists
        if os.path.exists(f"{self.vector_store_path}/index.faiss"):
            print("Loading existing vector store...")
            return FAISS.load_local(
                self.vector_store_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        
        # If not, create new vector store from local data
        print("Creating new vector store from local data...")
        return self._create_vector_store_from_local_data()

    def _create_vector_store_from_local_data(self):
        """Create vector store from local JSON data"""
        try:
            # Try to load from local JSON file
            json_path = "data/mental_health_resources/mental_health_dataset.json"
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Convert to documents
                docs = []
                for item in data:
                    # Make sure each item has the required fields
                    if "user_input" in item and "therapist_response" in item:
                        docs.append(Document(
                            page_content=f"Client: {item['user_input']}\nTherapist: {item['therapist_response']}",
                            metadata={
                                "emotion": item.get("emotion_label", ""),
                                "topic": item.get("topic", "general")
                            }
                        ))
                
                if not docs:
                    # Fallback to sample data if no valid documents
                    docs = self._get_sample_documents()
            else:
                # Fallback to sample data if file doesn't exist
                docs = self._get_sample_documents()
            
            # Create and save vector store
            vector_store = FAISS.from_documents(docs, self.embeddings)
            vector_store.save_local(self.vector_store_path)
            return vector_store
            
        except Exception as e:
            print(f"Error creating vector store from local data: {e}")
            # Fallback to sample data
            docs = self._get_sample_documents()
            vector_store = FAISS.from_documents(docs, self.embeddings)
            vector_store.save_local(self.vector_store_path)
            return vector_store

    def _get_sample_documents(self):
        """Get sample documents for fallback"""
        return [
            Document(
                page_content="Client: I'm feeling really anxious today.\nTherapist: I understand anxiety can be challenging. What specific thoughts or situations are triggering these feelings?",
                metadata={"emotion": "anxiety", "topic": "general"}
            ),
            Document(
                page_content="Client: I can't stop thinking negative thoughts.\nTherapist: Negative thought patterns can be difficult to break. Let's try to identify these thoughts and explore ways to reframe them.",
                metadata={"emotion": "depression", "topic": "general"}
            ),
            Document(
                page_content="Client: I'm having trouble sleeping lately.\nTherapist: Sleep issues can significantly impact our mental health. Could you share more about your bedtime routine and what might be keeping you awake?",
                metadata={"emotion": "stress", "topic": "sleep"}
            ),
            Document(
                page_content="Client: I feel overwhelmed with work and personal life.\nTherapist: Feeling overwhelmed can be exhausting. Let's break down what's happening and identify some manageable steps forward.",
                metadata={"emotion": "stress", "topic": "work-life"}
            ),
            Document(
                page_content="Client: I don't know how to handle my emotions.\nTherapist: Emotions can sometimes feel intense and confusing. Would you like to explore some emotional regulation techniques that might help?",
                metadata={"emotion": "general", "topic": "emotional-regulation"}
            )
        ]

    def load_hf_dataset(self):
        """Load and index HuggingFace dataset"""
        try:
            dataset = load_dataset(
                "Amod/mental_health_counseling_conversations",
                split="train[:1000]"  # Adjust based on your RAM
            )
            
            # Convert to documents
            docs = []
            for item in dataset:
                docs.append(Document(
                    page_content=f"Client: {item['user_input']}\nTherapist: {item['therapist_response']}",
                    metadata={
                        "emotion": item.get("emotion_label", ""),
                        "topic": item.get("topic", "general")
                    }
                ))
            
            # Add to vector store
            self.vector_store.add_documents(docs)
            self.vector_store.save_local(self.vector_store_path)
            print(f"Added {len(docs)} documents from HuggingFace dataset")
            
        except Exception as e:
            print(f"Dataset loading error: {e}")

    def get_context(self, query: str, emotion: str = "", k: int = 3) -> List[str]:
        """Retrieve context with emotion filtering"""
        filter_dict = {"emotion": emotion} if emotion else None
        try:
            docs = self.vector_store.similarity_search(
                query, 
                k=k, 
                filter=filter_dict
            )
            return [doc.page_content for doc in docs]
        except Exception as e:
            print(f"Retrieval error: {e}")
            # Return sample responses as fallback
            return [self._get_sample_documents()[0].page_content]