from fastapi import FastApi
from app.api.routes import router
from app.services.indexer import index_documents
from app.config import BOOK_PATH
import os
app = FastAPI()
app,include_router(router)

if __name__ =="__main__":
    if os.path.exists(BOOK_PATH):
        index_documents(BOOK_PATH)
    else:
        print("Arquivo para RAG não encontado. Verifique a existência do arquivo no caminho especificado.")