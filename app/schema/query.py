from pydantic import BaseModel, Field, field_validator

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Query string to search documents")

    @field_validator("query")
    def validate_query(cls, value):
        if not value.strip():
            raise ValueError("Query should not be empty.")
        return value
