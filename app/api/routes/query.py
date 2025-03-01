from fastapi import APIRouter, Depends, Request, HTTPException
from app.schema.query import QueryRequest
from app.services.retriever import DocumentRetriever

router = APIRouter()

def get_document_retriever(request: Request):
    if not request.state.retriever:
        raise HTTPException(
            status_code=503,
            detail="RAG system not completely available."
        )
    return request.state.retriever


@router.post("/query")
def query_documents(request: QueryRequest, retriever: DocumentRetriever = Depends(get_document_retriever)):
    try: 
        query = request.query.strip()

        if not query:
            raise HTTPException(status_code=400, detail="Query should not be empty.")
        
        result = retriever.query(query)
        sources = []

        if "source_documents" in result:
            sources = list({doc.metadata["source"] for doc in result["source_documents"] if "source" in doc.metadata})

        return {
            "response": result["response"],
            "sources": sources
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail= f"Error processing query: {str(e)}"
        )