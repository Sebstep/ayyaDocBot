from llama_index import StorageContext, load_index_from_storage

def loadvectorstorage():
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="./storage")

    # load index
    index = load_index_from_storage(storage_context)

    return index
