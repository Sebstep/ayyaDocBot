import os
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    ServiceContext,
    ListIndex,
    Document,
    SimpleDirectoryReader,
)
from llama_index.node_parser import SimpleNodeParser
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.storage.index_store import SimpleIndexStore
from llama_index.vector_stores import SimpleVectorStore, MilvusVectorStore
from llama_index.text_splitter import TokenTextSplitter


def build_new_storage(
    documents, type=["milvus", "simple"], storage_folder="storage", chunk_size=300
):
    if type == "milvus":
        vector_store = MilvusVectorStore(overwrite=True)
    elif type == "simple":
        vector_store = SimpleVectorStore()
    else:
        raise ValueError("type must be 'milvus' or 'simple'")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    service_context = ServiceContext.from_defaults(chunk_size=chunk_size)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, service_context=service_context, show_progress=True
    )
    index.storage_context.persist(persist_dir=f"{storage_folder}/{type}")
    return index
