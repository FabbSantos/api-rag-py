from pydantic import BaseModel, field_validator

class QueryRequest(BaseModel):
    query: str
    max_results: int = 5 # limitando pra lidar melhor

    @field_validator("query")
    def check_if_empty(cls, v):
        if not  v.strip():
            raise ValueError("Query não pode estar vazia.")
        return v

    @field_validator("max_results")
    def keep_reasonable(cls, v):
        if v <= 0 or v > 50:
            raise ValueError("Máximo de resultados tem que ser entre 1 e 50")
        return v
