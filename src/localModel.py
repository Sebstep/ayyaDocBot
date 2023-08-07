import os
from dotenv import load_dotenv

load_dotenv()
from transformers import AutoTokenizer, AutoModelForCausalLM

vicuna = "lmsys/vicuna-7b-v1.5-16k"
llama2 = "meta-llama/Llama-2-7b"


def download_hf_model(hf_slug):
    model_dir = "models/"

    maker, model_name = hf_slug.split("/", 1)
    new_location = os.path.join(model_dir, model_name)

    tokenizer = AutoTokenizer.from_pretrained(hf_slug)
    model = AutoModelForCausalLM.from_pretrained(hf_slug)

    tokenizer.save_pretrained(new_location)
    model.save_pretrained(new_location)


# download_hf_model(llama2)
