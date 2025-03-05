from fastapi import APIRouter, Depends, Request, HTTPException
from app.schema.query import QueryRequest
from app.services.retriever import DocumentRetriever
from app.utils.logger import logger

router = APIRouter()

def get_document_retriever(request: Request):
    if not hasattr(request.app.state, 'document_retriever') or not request.app.state.document_retriever:
        raise HTTPException(
            status_code=503,
            detail="RAG system not completely available."
        )
    return request.app.state.document_retriever

@router.post("/query")
def query_documents(request: QueryRequest, retriever: DocumentRetriever = Depends(get_document_retriever)):
    try:
        logger.info(f"Received query: {request.query}")
        # Passa a query original para o método query
        result = retriever.query(request.query)
        logger.info(f"Query completed with {len(result['sources'])} sources")
        return {
            "response": result["response"],
            "sources": result.get("sources", [])
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )