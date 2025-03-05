# app/services/indexer.py
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.utils.logger import logger
from app.utils.config import config
import os
import shutil

def index_documents(book_path: str):
    if os.path.exists(config.get_value("chroma.db_dir")) and len(os.listdir(config.get_value("chroma.db_dir"))) > 0:
        logger.info("Database already exists. Skipping indexing.")

    logger.info("Starting indexing...")
    os.makedirs(config.get_value("chroma.db_dir"), exist_ok=True)

    loader = TextLoader(book_path, encoding="utf-8")
    documents = loader.load()
    logger.info(f"Loaded document content: {documents[0].page_content[:200]}...")  # Debug inicial

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.get_value("chunking.chunk_size"),
        chunk_overlap=config.get_value("chunking.chunk_overlap"),
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    
    for chunk in chunks:
        chunk.metadata["source"] = book_path
        chunk.metadata["title"] = "On the Origin of Species"
    
    logger.info(f"Divided into {len(chunks)} chunks. First chunk: {chunks[0].page_content[:200]}...")

    embeddings = HuggingFaceEmbeddings(model_name=config.get_value("models.embedding"))
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=config.get_value("chroma.db_dir"),
        collection_name=config.get_value("chroma.collection_name")
    )
    collection = vector_store._collection
    logger.info(f"Collection {config.get_value('chroma.collection_name')} created with {len(chunks)} documents.")
    vector_store.persist()
    logger.info("Completed indexing.")