import os
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    ListIndex,
    Document,
    load_index_from_storage,
    SimpleDirectoryReader,
)
from llama_index.node_parser import SimpleNodeParser
from llama_index.text_splitter import TokenTextSplitter
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.storage.index_store import SimpleIndexStore
from llama_index.vector_stores import SimpleVectorStore
from llama_index.node_parser import SimpleNodeParser


def buildStorage(my_index_id):
    documents = SimpleDirectoryReader("documents/new").load_data()

    # create parser and parse document into nodes
    # how to customize: https://gpt-index.readthedocs.io/en/latest/core_modules/data_modules/index/usage_pattern.html#low-level-api
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(documents)

    # create storage context using default stores
    storage_context = StorageContext.from_defaults(
        docstore=SimpleDocumentStore(),
        vector_store=SimpleVectorStore(),
        index_store=SimpleIndexStore(),
    )

    # create (or load) docstore and add nodes
    storage_context.docstore.add_documents(nodes)

    # build index
    index = VectorStoreIndex(nodes, storage_context=storage_context)

    # save index locally
    index.set_index_id = my_index_id
    index.storage_context.persist(persist_dir="./storage")

    # move files from new to processed
    for fileName in os.listdir("documents/new"):
        old_file = os.getcwd() + "/documents/new/" + fileName
        new_file = os.getcwd() + "/documents/processed/" + fileName
        os.rename(old_file, new_file)

    return index


# def insertDoc(index):
#     document = SimpleDirectoryReader("documents/new").load_data()[0]
#     text_splitter = TokenTextSplitter(separator=" ", chunk_size=2048, chunk_overlap=20)
#     text_chunks = text_splitter.split_text(document.text)
#     doc_chunks = [Document(text=t) for t in text_chunks]

#     index = ListIndex([])
#     text_chunks = ["text_chunk_1", "text_chunk_2", "text_chunk_3"]

#     doc_chunks = []
#     for i, text in enumerate(text_chunks):
#         doc = Document(text=text, id_=f"doc_id_{i}")
#         doc_chunks.append(doc)

#     # insert
#     for doc_chunk in doc_chunks:
#         index.insert(doc_chunk)


def loadStorage():
    # load the persisted stores from persist_dir
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)
    return index
