import os, sys, argparse
from dotenv import load_dotenv
import logging
import openai
import streamlit


# setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("docbot.log"), logging.StreamHandler()],
)

# setup
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# run terminal
# os.system("python docbot/docbot.py")

# run streamlit
os.system("streamlit run docbot/guistreamlit.py")

# run flask
# os.system("python docbot/runflask.py")
