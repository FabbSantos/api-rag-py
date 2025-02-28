import os 

BOOK_PATH = "data/origin_of_species.md"


# ChromaDB
DB_DIR = "data/chromadb"
COLLECTION_NAME="origin_species"

# Chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Modelo
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "mistralai/Mistral-7B-Instruct"
