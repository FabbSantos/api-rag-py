from pydantic.v1 import BaseModel, Field
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.utils.config import config
from langchain_community.llms import Ollama

class DocumentRetriever(BaseModel):
    embeddings: HuggingFaceEmbeddings = Field(default=None)
    vector_store: Chroma = Field(default=None)
    llm: Ollama = Field(default=None)
    qa_chain: RetrievalQA = Field(default=None)

    class Config:
        arbitrary_types_allowed = True
        trust_immutable = True

    def __init__(self, **data):
        super().__init__(**data)
        self.embeddings = HuggingFaceEmbeddings(model_name=config.get_value("models.embedding"))
        self.vector_store = Chroma(
            persist_directory=config.get_value("chroma.db_dir"),
            embedding_function=self.embeddings,
            collection_name=config.get_value("chroma.collection_name")
        )

        # using local ollama
        self.llm = Ollama(
            model=config.get_value("models.llm"),
            base_url="http://localhost:11434"
        )
        
        self.qa_chain = self._initialize_qa_chain()

    def _initialize_qa_chain(self):
        retriever = self.vector_store.as_retriever(
            k=5,
            search_type="similarity",
            search_kwargs={'k': 5}
        )
        prompt_template = PromptTemplate(
            input_variables=["question", "documents"],
            template="""You are an assistant helping with questions about "On the Origin of Species" by Charles Darwin. Using the following context, provide a direct and clear answer.

            Context: {documents}
            Question: {question}
            Answer: Let me answer that directly -"""
        )

        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            input_key="question",
            output_key="response",
            return_source_documents=True,
            chain_type_kwargs={
                "prompt": prompt_template,
                "document_variable_name": "documents"
            }
        )

    def _calculate_confidence(self, result):
        if not result.get("source_documents"):
            return 0.0
        
        num_sources = len(result["source_documents"])
        response_length = len(result.get("response", ""))
        
        confidence = min((num_sources / 5) * 0.5 + (response_length / 500) * 0.5, 1.0)
        return round(confidence, 2)

    def _extract_sources(self, result):
        sources = []
        if "source_documents" in result:
            for doc in result.get("source_documents", []):
                if hasattr(doc, "metadata") and "source" in doc.metadata:
                    source = str(doc.metadata["source"])
                    if source and source not in sources:
                        sources.append(source)
        return sources

    def query(self, question: str):
        try:
            result = self.qa_chain.invoke({"question": question})
            response_text = result.get("response", "").strip()
            
            if not response_text:
                return {
                    "response": "No valid answer generated", 
                    "sources": [],
                    "confidence": 0.0
                }
                
            if len(response_text) < 10:
                return {
                    "response": "Response too short, please try again", 
                    "sources": [],
                    "confidence": 0.0
                }
                
            return {
                "response": response_text,
                "sources": self._extract_sources(result),
                "confidence": self._calculate_confidence(result)
            }
        except Exception as e:
            return {
                "response": f"Error processing query: {str(e)}", 
                "sources": [],
                "confidence": 0.0
            }
