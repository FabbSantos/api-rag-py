from fastapi import FastAPI, Request
from app.api.routes.query import router
from app.services.indexer import index_documents
from app.services.retriever import DocumentRetriever
from app.utils.logger import logger
import asyncio
import os

app = FastAPI(title="Origin of Species RAG")

@app.on_event("startup")
async def startup():
    logger.info("Ligando a API RAG")
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: index_documents("data/origin_of_species.md") if os.path.exists("data/origin_of_species.md") else logger.error("Arquivo do livro não encontrado."))
    app.state.retriever = DocumentRetriever()

app.include_router(router)