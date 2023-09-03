import os
import streamlit as st
import pandas as pd


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
