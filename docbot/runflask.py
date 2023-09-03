import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, jsonify, g
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
from filehelpers import list_files
from storageLogistics import build_new_storage


app = Flask(__name__)


# Create a context manager for the index
class IndexContext:
    def __init__(self):
        self.index = None

    def get_or_create_index(self):
        if self.index is None:
            self.load_index()
        return self.index

    def load_index(self):
        storage_folder = "storage"
        storage_context = StorageContext.from_defaults(
            persist_dir=f"./{storage_folder}"
        )
        self.index = load_index_from_storage(storage_context)

    def build_index(self):
        storage_folder = "storage"
        build_new_storage()
        self.load_index()


# Initialize the context manager
index_context = IndexContext()


# Route for the home page
@app.route("/", methods=["GET", "POST"])
def index():
    message = None  # Initialize the message variable

    if request.method == "POST":
        if request.form.get("action") == "load_index":
            index_context.get_or_create_index()
            message = "Index loaded successfully!"

            # Redirect to the chat interface after loading the index
            return redirect("/chat")

        elif request.form.get("action") == "build_index":
            index_context.build_index()
            message = "Index built successfully!"
            return redirect("/chat")

    return render_template(
        "index.html", message=message
    )  # Pass the message to the template


# Route for the chat interface page
@app.route("/chat", methods=["GET", "POST"])
def chat_interface():
    if request.method == "POST":
        user_input = request.form.get("user_input")

        # Get the index from the context manager
        index = index_context.get_or_create_index()

        # Initialize services and query engine
        llm = OpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=256)
        service_context = ServiceContext.from_defaults(llm=llm)
        set_global_service_context(service_context)
        retriever = VectorIndexRetriever(index=index, similarity_top_k=6)
        response_synthesizer = get_response_synthesizer(response_mode="refine")
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
            node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
        )

        # Process user input and generate a response
        response = query_engine.query(user_input)

        this_sources_list = []
        for source in response.source_nodes:
            source_dict = {
                "id": source.node.node_id,
                "text": source.node.text,
                "score": source.score,
            }
            this_sources_list.append(source_dict)

        chat_response = {
            "user": "User",
            "message": user_input,
            "bot": "Bot",
            "response": response.response,
            "sources": this_sources_list,
        }

        return jsonify(chat_response)

    return render_template("chat.html", chat_messages=[])


if __name__ == "__main__":
    app.run(debug=True)
