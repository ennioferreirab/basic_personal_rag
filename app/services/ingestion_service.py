import os

from chromadb import PersistentClient
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.extractors import KeywordExtractor, SummaryExtractor
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore

from app.core.config import settings


def ingest_documents():
    if not os.path.exists(settings.persist_directory):
        documents = SimpleDirectoryReader(settings.pdfs_folder).load_data()
        splitter = SentenceSplitter(chunk_size=512, chunk_overlap=20)
        extractors = [
            SummaryExtractor(summaries=["prev", "self"], llm=OpenAI(temperature=0.1, model=settings.model, max_tokens=100)),
            KeywordExtractor(keywords=10, llm=OpenAI(temperature=0.1, model=settings.model, max_tokens=50)),
        ]
        transformations = [splitter, *extractors]

        client = PersistentClient(path="db_rag")
        chroma_collection = client.get_or_create_collection("pdfs_completo")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

        pipeline = IngestionPipeline(
            documents=documents,
            transformations=transformations,
            project_name="base_conhecimento",
            docstore=SimpleDocumentStore(),
            vector_store=vector_store,
        )
        nodes = pipeline.run(show_progress=True)

        pipeline.persist(settings.persist_directory)
        index_store = VectorStoreIndex(nodes, show_progress=True)
        index_store.storage_context.persist(settings.persist_directory)
