import os, sys, argparse
from dotenv import load_dotenv
import openai
from llama_index import (
    StorageContext,
    ServiceContext,
    set_global_service_context,
    get_response_synthesizer,
    load_index_from_storage,
)
from llama_index.llms import OpenAI
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.indices.postprocessor import SimilarityPostprocessor
from storageLogistics import build_new_storage
import json
import time


# setup
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

args = False
# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--build", type=bool, default=False)
args = parser.parse_args()

storage_context = StorageContext.from_defaults(persist_dir="./storage")

if args.build:
    print("Building new storage...", flush=True)
    build_new_storage()
else:
    # load vector store
    print("Loading existing storage...", flush=True)
    index = load_index_from_storage(storage_context)


# define LLM
llm = OpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=256)

# configure service context
service_context = ServiceContext.from_defaults(llm=llm)
set_global_service_context(service_context)

# # # # # # # # # # # # # # # #
# Retriever and synthesizer
#
# How-to. https://gpt-index.readthedocs.io/en/latest/core_modules/model_modules/llms/usage_custom.html

# configure retriever
# defines how to retrieve relevant nodes from the index
# how to: https://gpt-index.readthedocs.io/en/latest/core_modules/query_modules/retriever/root.html
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=4,
)

# configure response synthesizer
# After a retriever fetches relevant nodes, a BaseSynthesizer synthesizes the final response by combining the information.
response_synthesizer = get_response_synthesizer(response_mode="refine")

# assemble query engine
# An index can have a variety of index-specific retrieval modes.
# For instance, a list index supports the default ListIndexRetriever that retrieves all nodes,
# and ListIndexEmbeddingRetriever that retrieves the top-k nodes by embedding similarity.
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
)

# prepare to save the output
all_responses_dict = {}
counter = 0
timestamp = int(time.time())
output_dir = os.makedirs("output", exist_ok=True)
output_file = os.path.abspath(f"output/{timestamp}_chat_output.txt")


# start the chat
while True:
    my_query = input("User: ")
    response = query_engine.query(my_query)

    print(f"Agent: {response.response}", flush=True)
    print(f"Sources: {response.get_formatted_sources()}", flush=True)

    this_sources_dict = {}
    for source in response.source_nodes:
        this_sources_dict["id"] = source.node.node_id
        this_sources_dict["text"] = source.node.text
        this_sources_dict["score"] = source.score

    this_response_dict = {}
    this_response_dict = {
        "query": my_query,
        "response": response.response,
        "sources": json.dumps(this_sources_dict),
    }

    all_responses_dict[counter] = this_response_dict

    with open(output_file, "w") as f:
        json.dump(all_responses_dict, f)

    counter += 1
