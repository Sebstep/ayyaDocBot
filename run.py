import os, sys, argparse
from dotenv import load_dotenv
import logging


# setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("docbot.log"), logging.StreamHandler()],
)


# run terminal
# os.system("python docbot/docbot.py")

# run streamlit
os.system("streamlit run docbot/guistreamlit.py")

# run flask
# os.system("python docbot/runflask.py")
