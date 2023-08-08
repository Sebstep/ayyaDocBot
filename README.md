# Introduction

A chatbot-to-be for a knowledge-base-to-be.

## Setup

- `mv .env.template .env` to rename the .env file
- Create a virtual environment with `python -m venv venv` or `conda create -n <envname>`
- `pip install -r requirements.txt` or `conda install --file requirements.txt`
- 

## Usage

- `documents`: folder contains the documents to be indexed for the knowledge base
  - `.new`: files here are to be inserted into an existing index
  - `.processed`: documents are moved to after being indexed
- `llms`: large model files
- `src`: python scripts
  - `docbot.py`: runs the chatbot; can create the local index if it doesn't exist
  - `localModelDownlaod.py`: download llms from huggingface
  - `storageLogistics.py`: function to create or append to local index


## Roadmap

- [x] Create local index of documents
- [ ] Make it possible to insert new documents into existing local index
- [x] Create working Q&A pipeline for documents in the local index
- [ ] Switch LLM from OpenAI-API to local model (llama2 / vicuna / bloom / etc.)


# Documentations

- [Tool Stack Architecture](https://a16z.com/2023/06/20/emerging-architectures-for-llm-applications/)

## Packages

- [LlamaIndex](https://gpt-index.readthedocs.io/en/latest/end_to_end_tutorials/usage_pattern.html)
- [Huggingface Transformers](https://github.com/huggingface/transformers)
- [LangChain](https://docs.langchain.com/docs/) soon
