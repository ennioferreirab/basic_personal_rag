from textwrap import dedent

from llama_index.core import PromptTemplate, StorageContext, load_index_from_storage
from llama_index.core.query_pipeline import QueryPipeline
from llama_index.core.retrievers.fusion_retriever import QueryFusionRetriever
from llama_index.llms.openai import OpenAI
from llama_index.retrievers.bm25 import BM25Retriever

from app.core.config import settings


def query_pipeline(question: str):
    storage_context = StorageContext.from_defaults(persist_dir=settings.persist_directory)
    index_store = load_index_from_storage(storage_context=storage_context)

    vector_retriever = index_store.as_query_engine()
    bm25_retriever = BM25Retriever.from_defaults(docstore=storage_context.docstore)
    hybrid_retriever = QueryFusionRetriever(
        [vector_retriever, bm25_retriever],
        similarity_top_k=5,
        num_queries=5,
        mode="reciprocal_rerank",
        use_async=True,
        verbose=True,
    )

    prompt_initial_str = dedent(
        """
        Retrieve all relevant context documents for the following question, 
        focusing on detailed explanations of the key concepts:
        Question: {query_str}
        """
    )
    prompt_final_str = dedent(
        """
        Please act as a detailed reference consultant. Provide a comprehensive, thorough, 
        and detailed answer to the following question based on the provided context documents. 
        Ensure that your response emphasizes detailed explanations of the key 
        concepts and does not prioritize examples of use cases.

        Context documents: {context_docs}
        Detailed Answer:
        """
    )

    prompt_initial = PromptTemplate(prompt_initial_str)
    prompt_final = PromptTemplate(prompt_final_str)
    llm = OpenAI(model="gpt-4o", temperature=0.1)

    p = QueryPipeline(verbose=True)

    p.add_modules(
        {
            "prompt_initial": prompt_initial,
            "llm": llm,
            "hybrid_retriever": hybrid_retriever,
            "prompt_final": prompt_final,
        }
    )

    p.add_link("prompt_initial", "hybrid_retriever")
    p.add_link("hybrid_retriever", "prompt_final", dest_key="context_docs")
    p.add_link("prompt_final", "llm", dest_key="messages")

    output, _ = p.run_with_intermediates(question)
    return output.message.content
