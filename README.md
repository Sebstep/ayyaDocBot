# Introduction

A chatbot-to-be for a knowledge-base-to-be.

## Setup

- `mv .env.template .env` to rename the .env file

## Usage

- `documents`: folder contains the documents to be indexed for the knowledge base
  - `.new`: files here are to be inserted into an existing index
  - `.processed`: documents are moved to after being indexed
- `llms`: large model files
- `src`: python scripts
  - `docbot.py`: runs the chatbot; use `python src/docbot.py --build=true` to build a new index
  - `localModelDownlaod.py`: download llms from huggingface
  - `storageLogistics.py`: functions to build or update the local index

## Roadmap

- [x] Create local index of documents
- [x] Create working Q&A pipeline for documents in the local index
- [ ] Make it possible to insert new documents into existing local index (rather than always building an entirely new index)
- [ ] Setup more extensive metadata for the local index to improve results
- [ ] Setup [AutoMergingRetriever](https://www.linkedin.com/feed/update/urn:li:activity:7102507748361142273/)
- [ ] Experiment with chunk lengths. Sentenes/paragraphs?
- [ ] Switch LLM from OpenAI-API to local model (llama2 / vicuna / bloom / etc.), see [here](https://www.youtube.com/watch?v=njzB6fm0U8g)
- [ ] Switch local vector database to (e.g., "faiss" or "chromaDB")
- [ ] Attach a continuous learning database that grows over time
- [ ] Add guardrails

# Documentations

- [Tool Stack Architecture](https://a16z.com/2023/06/20/emerging-architectures-for-llm-applications/)
- [Which Index Structure to Use](https://www.mikulskibartosz.name/llama-index-which-index-should-you-use/) (docstore/vectorstore/knowledgegraph)
- [Prompting Guide](https://www.promptingguide.ai/)

## Packages

- [LlamaIndex](https://gpt-index.readthedocs.io/en/latest/end_to_end_tutorials/usage_pattern.html)
- [Huggingface Transformers](https://github.com/huggingface/transformers)
- [LangChain](https://docs.langchain.com/docs/) soon

# Misc.

## Using llama with Huggingface

- Get approval from Meta: https://ai.meta.com/resources/models-and-libraries/llama-downloads/
- Get approval from HF: https://huggingface.co/meta-llama/Llama-2-7b
- Create a read token from here: https://huggingface.co/settings/tokens
- `pip install transformers`
- execute `huggingface-cli` login and provide read token
- Execute your code. It should work fine.
