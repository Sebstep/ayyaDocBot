import os
import streamlit as st
import pandas as pd
import json
import time
import pickle


def parse_response(user_input, response):
    # Parse response

    this_sources_list = []
    for source in response.source_nodes:
        source_dict = {
            "id": source.node.node_id,
            "text": source.node.text,
            "score": source.score,
            "file_name": source.node.metadata["file_name"],
        }
        this_sources_list.append(source_dict)

    parsed_response_dict = {
        "message": user_input,
        "response": response.response,
        "sources": this_sources_list,
    }

    return parsed_response_dict


def save_response_to_json(chat_response, OUTPUT_FOLDER):
    timestamp = time.strftime("%Y%m%d%H%M%S")
    output_json_file = os.path.join(OUTPUT_FOLDER, f"{timestamp}_chat_output.txt")

    with open(output_json_file, "w") as f:
        json.dump(chat_response, f)
    return output_json_file


def display_response(parsed_response_dict):
    st.write(parsed_response_dict["response"])


def display_sources(parsed_response_dict):
    count = 1
    for source in parsed_response_dict["sources"]:
        with st.expander(f"Source {count} Similarity: {round(source['score'], 5)}, File: " + source["file_name"]):
            st.write(f"Node-ID: {source['id']}")
            st.write(f"{source['text']}")
        count += 1


def get_df_files(folder):
    if not os.path.exists(folder):
        st.write(f"The location '{folder}' does not exist.")
        return

    st.write(f"Files found at '{folder}': ")

    files = os.listdir(folder)

    file_info_list = []

    for file_name in files:
        file_path = os.path.join(folder, file_name)
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = file_size_bytes / 1024 / 1024
        file_size = round(file_size_mb, 2)
        file_creation_date = os.path.getctime(file_path)
        file_info = {
            "File Name": file_name,
            "Size (MB)": file_size,
            "Created Date": file_creation_date,
        }
        file_info_list.append(file_info)

    # Create a DataFrame from the list of file info dictionaries
    file_info_df = pd.DataFrame(file_info_list)

    return file_info_df
