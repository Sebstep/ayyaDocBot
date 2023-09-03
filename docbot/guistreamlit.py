import os
import openai
from dotenv import load_dotenv
import streamlit as st
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

import logging
from localhelpers import (
    parse_response,
    save_response_to_json,
    display_response,
    display_sources,
)
from langchain.chat_models import ChatOpenAI


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("docbot.log"), logging.StreamHandler()],
)

# constants
STORAGE_FOLDER = "storage"
OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@st.cache_resource
def get_index():
    index = load_index_from_storage(
        StorageContext.from_defaults(persist_dir=f"{STORAGE_FOLDER}"),
    )
    return index


def is_api_key_valid():
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt="This is a test.",
            max_tokens=5
        )
    except:
        return False
    else:
        return True


# Initialize Streamlit
st.title("Document Q&A")



# Create a sidebar with options
with st.sidebar:
    st.sidebar.header("Navigation")
    selected_option = st.sidebar.radio("Pages:", ["Manage", "Chat"])


##########################################
# MANAGE PAGE
##########################################
if selected_option == "Manage":
    st.subheader("Manage Index")

    openai_keystring = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

    if st.button("Load Models"):
        if not openai.api_key:
            openai.api_key = openai_keystring
            if not is_api_key_valid():
                st.error("Invalid API key.")
        with st.spinner("Loading models..."):
            index = get_index()
        st.success("Models loaded!")

    st.divider()

    "Warning, building a new index takes very long."

    if st.button("Build New Index"):
        with st.spinner("Building new index..."):
            build_new_storage()
        st.success("New index built!")

    # st.write(get_index().ref_doc_info)

    # st.write("To upload a new file into the index, use the file uploader below.")
    # uploaded_file = st.file_uploader("Choose a file")
    # if uploaded_file is not None:
    #     with open(os.path.join("documents/uploads",uploaded_file.name),"wb") as f:
    #         f.write(uploaded_file.getbuffer())



##########################################
# CHAT PAGE
##########################################
if selected_option == "Chat":

    st.subheader("LLM Settings")

    col_temp, col_tokens = st.columns(2)

    with col_temp:
        temperature = st.slider(
            label="LLM temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.05,
            help="How creative the LLM should be",
        )

    with col_tokens:
        max_tokens = st.slider(
            label="Max. Tokens",
            min_value=64,
            max_value=2048,
            value=64,
            step=64,
            help="How many tokens to generate",
        )

    col_topk, col_model = st.columns(2)

    with col_topk:
        top_k_nodes = st.number_input(
            label="Similarity Top K",
            min_value=1,
            max_value=20,
            value=1,  # set to 6-8 or more for production
            step=1,
            help="How many similar nodes to return and summarize",
        )

    with col_model:
        model = st.selectbox(
            "Model", ["gpt-3.5-turbo", "gpt-4"], help="Which model to use"
        )

    llm = OpenAI(model=model, temperature=temperature, max_tokens=max_tokens)

    service_context = ServiceContext.from_defaults(llm=llm)

    retriever = VectorIndexRetriever(index=get_index(), similarity_top_k=top_k_nodes)

    response_synthesizer = get_response_synthesizer(response_mode="refine")

    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
    )

    # input
    st.subheader("Prompt")
    user_input = st.text_input("Enter your message:", key="prompt")
    if st.button("Send"):
        with st.chat_message("User", avatar="🙋‍♂️"):
            st.write(user_input)
        with st.spinner("Getting response..."):
            response = query_engine.query(user_input)
        st.success("Response received!")
        parsed_response_dict = parse_response(user_input, response)
        output_json_file = save_response_to_json(parsed_response_dict, OUTPUT_FOLDER)
        st.toast(f"Saved to:  {output_json_file}", icon="💾")
        with st.chat_message("Bot", avatar="🤖"):
            display_response(parsed_response_dict)
            display_sources(parsed_response_dict)


# Run Streamlit app
if __name__ == "__main__":
    st.sidebar.text("Streamlit App")
