import os
from transformers import AutoTokenizer, AutoModelForCausalLM


# huggingface model-slugs
vicuna = "lmsys/vicuna-7b-v1.5-16k"
llama2 = "meta-llama/Llama-2-7b"


def download_hf_model(hf_slug: str):
    print(
        "\033[93m"
        + "Warning: Model download can take a VERY long time."
        + "\033[0m"
        + "\nYou should have at least 2x the model size in free disk space.",
        flush=True,
    )
    decision = input("To continue, type 'y' and press enter.\nResponse: ")

    if decision == "y":
        model_dir = os.path.abspath("llms")

        maker, model_name = hf_slug.split("/", 1)
        new_location = os.path.join(model_dir, model_name)

        # download tokenizer and model to /Users/<current_user>/.cache
        tokenizer = AutoTokenizer.from_pretrained(hf_slug)
        model = AutoModelForCausalLM.from_pretrained(hf_slug)

        # move files from cache to project dir /models
        tokenizer.save_pretrained(new_location)
        model.save_pretrained(new_location)

        print(
            "\033[92m"
            + f"Model '{model_name}' downloaded to {new_location}"
            + "\033[92m",
            flush=True,
        )


download_hf_model(vicuna)
# download_hf_model(llama2) # not yet openly available
