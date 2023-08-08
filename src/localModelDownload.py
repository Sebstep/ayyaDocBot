import os
from transformers import AutoTokenizer, AutoModelForCausalLM


# huggingface model-slugs
vicuna = "lmsys/vicuna-7b-v1.5-16k"
llama2 = "meta-llama/Llama-2-7b"


def download_hf_model(hf_slug: str):
    print = "Warning: Model download can take a VERY long time."
    print = "You should have at least 2x the model size in free disk space."
    input = input("Continue? Press: y")

    if input == "y":
        model_dir = os.path.abspath("llms")

        maker, model_name = hf_slug.split("/", 1)
        new_location = os.path.join(model_dir, model_name)

        # download tokenizer and model to /Users/<current_user>/.cache
        tokenizer = AutoTokenizer.from_pretrained(hf_slug)
        model = AutoModelForCausalLM.from_pretrained(hf_slug)

        # move files from cache to project dir /models
        tokenizer.save_pretrained(new_location)
        model.save_pretrained(new_location)

        print("Model downloaded to " + new_location)


# # only activate if needed
# download_hf_model(vicuna)
# download_hf_model(llama2)
