import os
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    ListIndex,
    Document,
    SimpleDirectoryReader,
)
from llama_index.node_parser import SimpleNodeParser
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.storage.index_store import SimpleIndexStore
from llama_index.vector_stores import SimpleVectorStore
from llama_index.text_splitter import TokenTextSplitter
from llama_index.node_parser.extractors import (
    MetadataExtractor,
    SummaryExtractor,
    QuestionsAnsweredExtractor,
    TitleExtractor,
    KeywordExtractor,
    EntityExtractor,
)


def set_node_parser(chunk_size):
    metadata_extractor = MetadataExtractor(
        extractors=[
            # TitleExtractor(nodes=5),
            # QuestionsAnsweredExtractor(questions=3),
            # SummaryExtractor(summaries=["prev", "self"]),
            # KeywordExtractor(keywords=10),
            # EntityExtractor(prediction_threshold=0.5),
        ],
    )

    node_parser = SimpleNodeParser.from_defaults(
        chunk_size=chunk_size,
        metadata_extractor=metadata_extractor,
    )

    return node_parser


def build_new_storage():
    # load documents from directory
    documents = SimpleDirectoryReader("documents/new", filename_as_id=True).load_data()

    # parse document into nodes
    node_parser = set_node_parser(300)
    nodes = node_parser.get_nodes_from_documents(documents, show_progress=True)

    # create storage context using default stores
    storage_context = StorageContext.from_defaults(
        docstore=SimpleDocumentStore(),
        index_store=SimpleIndexStore(),
        vector_store=SimpleVectorStore(),
    )

    # create (or load) docstore and add nodes
    storage_context.docstore.add_documents(nodes)

    # build index
    vector_index = VectorStoreIndex(nodes, storage_context=storage_context)

    # save index locally
    # if you have multiple indices, add a uniqe id for each
    # index.set_index_id = my_index_id
    vector_index.storage_context.persist(persist_dir="./storage")

    return vector_index


# def insert_doc(document, index):
#     storage_context = StorageContext.from_defaults(
#         docstore=SimpleDocumentStore(),
#         index_store=SimpleIndexStore(),
#         vector_store=SimpleVectorStore(),
#     )

#     node_parser = set_node_parser(300)
#     nodes = node_parser.get_nodes_from_documents(document)

#     storage_context.docstore.add_documents(nodes)

#     for node in nodes:
#         index.insert(node)
