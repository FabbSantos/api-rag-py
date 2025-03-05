from fastapi import FastAPI, Request
from app.api.routes.query import router
from app.services.indexer import index_documents
from app.services.retriever import DocumentRetriever
from app.utils.logger import logger
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Origin of Species RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def startup_event():
    logger.info("Ligando a API RAG")
    if os.path.exists("data/origin_of_species.md"):
        index_documents("data/origin_of_species.md")
    else:
        logger.error("Arquivo do livro não encontrado")
    app.state.document_retriever = DocumentRetriever()

app.on_event("startup")(startup_event)

app.include_router(router)