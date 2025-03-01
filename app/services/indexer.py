from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from app.config import DB_DIR, COLLECTION_NAME, CHUNK_SIZE, CHUNK_OVERLAP
import os 

def index_documents(book_path: str):
    
    # checks if db exists
    if os.path.exists(DB_DIR) and len(os.listdir(DB_DIR)) > 0:
        print("Database already exists. Skipping indexing.")
        return
    
    print("Starting indexing...")
    os.makedirs(DB_DIR, exist_ok=True)

    loader = TextLoader(book_path, encoding="utf-8")
    documents = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Divided into {len(chunks)} chunks.")

    # Create embeddings and saving in chroma
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", api_key=os.getenv("HUGGING_FACE_API_KEY"))
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR,
        collection_name=COLLECTION_NAME
    ) 
    vector_store.persist()
    print("Completed indexing.")