from fastapi import FastAPI
from app.api.routes.query import router
from app.services.indexer import index_documents
from app.config import BOOK_PATH
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
app = FastAPI()
app.include_router(router)

if __name__ =="__main__":
    if os.path.exists(BOOK_PATH):
        index_documents(BOOK_PATH)
    else:
        print("Arquivo para RAG não encontado. Verifique a existência do arquivo no caminho especificado.")