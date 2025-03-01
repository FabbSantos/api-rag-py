from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.utils.config import config
import os 
class DocumentRetriever:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=config.get_value("models.embedding"))
        self.vector_store = Chroma(
            persist_directory=config.get_value("chroma.db_dir"),
            embedding_function=self.embeddings,
            collection_name=config.get_value("chroma.collection_name")
        )
        self.llm = HuggingFacePipeline(pipeline=pipeline("text-generation", model=config.get_value("models.llm")))
        self.qa_chain = self._initialize_qa_chain()

    def _initialize_qa_chain(self):
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )

    def query(self, question: str):
        if not question.strip():
            raise ValueError("A pergunta não pode estar vazia.")

        result = self.qa_chain({"query": question})

        sources = []
        if "source_documents" in result:
            for doc in result["source_documents"]:
                if hasattr(doc, "metadata") and "source" in doc.metadata:
                    source = doc.metadata["source"]
                    if source not in sources:
                        sources.append(source)

        return {
            "response": result.get("result", "No answer found."),
            "sources": sources
        }