from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.retriever import DocumentRetriever

router = APIRouter()

class QueryRequest(BaseModel):
    query: str


@router.post("/query")
def query_documents(request: QueryRequest):
    try: 
        retriever = DocumentRetriever()

        if not retriever: 
            raise HTTPException(
                status_codde=503,
                detail="RAG system not completely available."
            )
        
        query = request.query.strip()
        if not query:
            raise HTTPException(
                status_code=400,
                detail="Query should not be empty."
            )
        
        result = retriever({"query": query})
        sources = []

        if "source_documents" in result:
            sources = list({doc.metadata["source"] for doc in result["source_documents"] if "source" in doc.metadata})

        return {
            "response": result["result"],
            "sources": sources
        }
    except Exception as e:
        raise HHTPException(
            status_code=500,
            detail= f"Error processing query: {str(e)}"
        )