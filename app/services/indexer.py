# app/services/indexer.py
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.utils.logger import logger
from app.utils.config import config
import os

def index_documents(book_path: str):
    # checks if db exists
    if os.path.exists("data/chromadb") and len(os.listdir("data/chromadb")) > 0:
        logger.info("Database already exists. Skipping indexing.")
        return
    
    logger.info("Starting indexing...")
    os.makedirs("data/chromadb", exist_ok=True)

    loader = TextLoader(book_path, encoding="utf-8")
    documents = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Divided into {len(chunks)} chunks.")

    # Create embeddings and saving in chroma
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="data/chromadb",
        collection_name="origin_species"
    )
    vector_store.persist()
    logger.info("Completed indexing.")