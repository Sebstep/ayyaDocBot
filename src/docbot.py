from dotenv import load_dotenv
import os
import openai
from llama_index import (
    ServiceContext,
    set_global_service_context,
    get_response_synthesizer,
)
from llama_index.llms import OpenAI
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.indices.postprocessor import SimilarityPostprocessor
from src.storageLogistics import buildStorage, loadStorage

# setup
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# load vector store
index = loadStorage()

# define LLM
llm = OpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=256)

# configure service context
service_context = ServiceContext.from_defaults(llm=llm)
set_global_service_context(service_context)

# See the Custom LLM’s How-To for more details. https://gpt-index.readthedocs.io/en/latest/core_modules/model_modules/llms/usage_custom.html

# configure retriever
# defines how to retrieve relevant nodes from the index
# how to: https://gpt-index.readthedocs.io/en/latest/core_modules/query_modules/retriever/root.html
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=2,
)

# configure response synthesizer
# After a retriever fetches relevant nodes, a BaseSynthesizer synthesizes the final response by combining the information.
response_synthesizer = get_response_synthesizer()

# assemble query engine
# An index can have a variety of index-specific retrieval modes.
# For instance, a list index supports the default ListIndexRetriever that retrieves all nodes,
# and ListIndexEmbeddingRetriever that retrieves the top-k nodes by embedding similarity.
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
)

while True:
    response = query_engine.query(input("User: "))
    print(f"Agent: {response}")
