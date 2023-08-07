import os
from llama_index import StorageContext, load_index_from_storage
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    ListIndex,
    Document,
)
from llama_index.node_parser import SimpleNodeParser
from llama_index.text_splitter import TokenTextSplitter


def buildStorage():
    documents = SimpleDirectoryReader("documents/new").load_data()
    index = VectorStoreIndex.from_documents(documents)
    storage_context = StorageContext.from_defaults()
    index.storage_context.persist(persist_dir="./storage")
    for fileName in os.listdir("documents/new"):
        old_file = os.getcwd() + "/documents/new/" + fileName
        new_file = os.getcwd() + "/documents/processed/" + fileName
        os.rename(old_file, new_file)
    return index


def insertDoc(index):
    document = SimpleDirectoryReader("documents/new").load_data()[0]
    text_splitter = TokenTextSplitter(separator=" ", chunk_size=2048, chunk_overlap=20)
    text_chunks = text_splitter.split_text(document.text)
    doc_chunks = [Document(text=t) for t in text_chunks]

    index = ListIndex([])
    text_chunks = ["text_chunk_1", "text_chunk_2", "text_chunk_3"]

    doc_chunks = []
    for i, text in enumerate(text_chunks):
        doc = Document(text=text, id_=f"doc_id_{i}")
        doc_chunks.append(doc)

    # insert
    for doc_chunk in doc_chunks:
        index.insert(doc_chunk)


def loadStorage():
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)
    return index
