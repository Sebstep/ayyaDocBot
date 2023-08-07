# Introduction

A chatbot-to-be for a knowledge-base-to-be.

## Usage

```bash
# rename .env file
mv .env.template .env
```

### Create virtual environment

With conda

```bash
conda env create -f environment.yml
conda activate docbot
```

With pip

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Start the bot

```bash
python -m src/docbot
```


# Dependencies' Documentations

- [LlamaIndex](https://gpt-index.readthedocs.io/en/latest/end_to_end_tutorials/usage_pattern.html)
- [Huggingface Transformers](https://github.com/huggingface/transformers)
- [LangChain](https://docs.langchain.com/docs/) soon
