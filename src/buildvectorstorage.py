# Data preprocessing / embedding: 
# This stage involves storing private data (legal documents, in our example) to be retrieved later. 
#
# Typically, the documents are broken into chunks, 
# passed through an embedding model, 
# then stored in a specialized database called a vector database.

from dotenv import load_dotenv
load_dotenv()

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index import VectorStoreIndex, SimpleDirectoryReader

# builds an index over the documents in the data folder (which in this case just consists of the essay text
documents = SimpleDirectoryReader('input').load_data()

from llama_index.node_parser import SimpleNodeParser

parser = SimpleNodeParser()

nodes = parser.get_nodes_from_documents(documents)

from llama_index import StorageContext

index = VectorStoreIndex(nodes)

storage_context = StorageContext.from_defaults()





query_engine = index.as_query_engine()

response = query_engine.query(input("Query: "))

print(response)

# The next step is to parse these Document objects into Node objects. 
# Nodes represent “chunks” of source Documents, whether that is a text chunk, an image, or more. 
# They also contain metadata and relationship information with other nodes and index structures.


# save index to ./storage
index.storage_context.persist()
