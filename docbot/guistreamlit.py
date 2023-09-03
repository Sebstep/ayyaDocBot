import os
import time
import openai
from dotenv import load_dotenv
import streamlit as st
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
import logging
from filehelpers import get_df_files

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("docbot.log"), logging.StreamHandler()],
)

# Initialize Streamlit
st.title("Document Q&A")


@st.cache_resource
def get_index():
    storage_folder = "storage"
    storage_context = StorageContext.from_defaults(persist_dir=f"./{storage_folder}")
    index = load_index_from_storage(storage_context)
    return index


index = get_index()

# Create a sidebar with options
with st.sidebar:
    st.sidebar.header("Navigation")
    selected_option = st.sidebar.radio("Pages:", ["Manage Index", "Chat"])

    # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

# Route for the home page
if selected_option == "Manage Index":
    st.subheader("Manage Index")

    if st.button("Load Index"):
        with st.status("Loading index..."):
            index = get_index()
        st.success("Index loaded successfully!")

    # if st.button("Rebuild Index"):
    #     with st.status("Building index..."):
    #         build_index()
    #     st.success("Index built successfully!")

    if st.button("Get index state"):
        st.write("The index is live? ", index is not None)

    st.write("To upload a new file into the index, use the file uploader below.")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()


# Route for the chat interface page
if selected_option == "Chat":
    st.subheader("LLM Settings")

    col1, col2 = st.columns(2)

    with col1:
        temperature = st.slider(
            label="LLM temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.05,
            help="How creative the LLM should be",
        )

    with col2:
        max_tokens = st.slider(
            "Max. Tokens", 0, 4096, 512, 16, help="How many tokens to generate"
        )

    col3, col4 = st.columns(2)

    with col3:
        similarity_top_k = st.number_input(
            "Similarity Top K",
            2,
            20,
            8,
            1,
            help="How many similar nodes to return and summarize",
        )

    with col4:
        model = st.selectbox(
            "Model", ["gpt-3.5-turbo", "gpt-4"], help="Which model to use"
        )

    # Initialize services and query engine
    llm = OpenAI(model=model, temperature=temperature, max_tokens=max_tokens)
    service_context = ServiceContext.from_defaults(llm=llm)
    set_global_service_context(service_context)
    retriever = VectorIndexRetriever(
        index=get_index(), similarity_top_k=similarity_top_k
    )
    response_synthesizer = get_response_synthesizer(response_mode="refine")
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
    )

    # input
    st.subheader("Prompt")
    user_input = st.text_input("Enter your message and hit enter:")
    if user_input:
        with st.status("Awaiting response..."):
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
            "message": user_input,
            "response": response.response,
            "sources": this_sources_list,
        }

        # save response locally
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)
        timestamp = time.strftime("%Y%m%d%H%M%S")
        output_file = os.path.join(output_folder, f"{timestamp}_chat_output.txt")
        with open(output_file, "w") as f:
            json.dump(chat_response, f)

        # output response
        st.header("Chat Response")
        st.write("User: ", chat_response["message"])
        st.write("Bot: ", chat_response["response"])
        st.toast(f"Saved to:  {output_file}", icon="💾")

        st.header("Sources:")
        count = 1
        for source in this_sources_list:
            st.subheader(f"Source {count}:")
            st.write(f"Similarity: {source['score']} - ID: {source['id']}")
            with st.expander("See source text"):
                st.write(f"{source['text']}")
            count += 1


# Run Streamlit app
if __name__ == "__main__":
    st.sidebar.text("Streamlit App")
