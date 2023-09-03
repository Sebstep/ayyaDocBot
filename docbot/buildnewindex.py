import openai
from dotenv import load_dotenv

import os, argparse
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

# define LLM

# setup
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=256)
storage_folder = os.getenv("STORAGE_FOLDER")
output_folder = os.getenv("OUTPUT_FOLDER")

build_new_storage()