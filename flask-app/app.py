import os
import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from llama_index import (
    StorageContext,
    ServiceContext,
    get_response_synthesizer,
    load_index_from_storage,
)
from llama_index.llms import OpenAI
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.indices.postprocessor import SimilarityPostprocessor
from storageLogistics import build_new_storage
from localhelpers import (
    parse_response,
    save_response_to_json,
    display_response,
    display_sources,
)

app = Flask(__name__)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Constants
STORAGE_FOLDER = "storage"
OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Initialize the index
index = load_index_from_storage(
    StorageContext.from_defaults(persist_dir=f"{STORAGE_FOLDER}")
)


# Check if the API key is valid
def is_api_key_valid():
    try:
        response = openai.Completion.create(
            engine="davinci", prompt="This is a test.", max_tokens=5
        )
    except:
        return False
    else:
        return True


# Routes


@app.route("/")
def index_page():
    return redirect(url_for("chat"))


@app.route("/manage")
def manage():
    return render_template("manage.html")


@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.form["user_input"]

        # LLM settings
        model = request.form["model"]
        max_tokens = int(request.form["max_tokens"])
        top_k_nodes = int(request.form["top_k_nodes"])
        temperature = float(request.form["temperature"])

        llm = OpenAI(model=model, temperature=temperature, max_tokens=max_tokens)
        service_context = ServiceContext.from_defaults(llm=llm)

        retriever = VectorIndexRetriever(index=index, similarity_top_k=top_k_nodes)
        response_synthesizer = get_response_synthesizer(response_mode="refine")
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
            node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
        )

        response = query_engine.query(user_input)
        parsed_response_dict = parse_response(user_input, response)
        output_json_file = save_response_to_json(parsed_response_dict, OUTPUT_FOLDER)

        return render_template(
            "chat.html",
            openai_key=openai.api_key,
            response=parsed_response_dict,
            json_file=output_json_file,
        )

    return render_template("chat.html", openai_key=openai.api_key)


if __name__ == "__main__":
    app.run(debug=True)
