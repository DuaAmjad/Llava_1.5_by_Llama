# -*- coding: utf-8 -*-
"""LLAVA 1.5 By LLAMA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14N27HMrN3cn48vDI4XhxNCcoqMuAGB_a
"""

#LLAMA INTEGRATION
#iMAGE ANALYSIS
#BY DUA AMJAD

# Install required libraries
!pip install -q -U transformers==4.37.2
!pip install -q bitsandbytes==0.41.3 accelerate==0.25.0

import torch
from transformers import BitsAndBytesConfig, pipeline
from PIL import Image
import re
import textwrap  #for wrapping text

# Configuration for LLaMA model
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)
model_id = "llava-hf/llava-1.5-7b-hf"
pipe = pipeline("image-to-text",
                model=model_id,
                model_kwargs={"quantization_config": quantization_config})

# Function to describe an image
def describe_image(image_path):
    image = Image.open(image_path)
    prompt_instructions = """
    Describe the image using as much detail as possible. Mention if it is a painting, a photograph, predominant colors, and what the image is about.
    """
    prompt = "USER: <image>\n" + prompt_instructions + "\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # Extract the response text
    match = re.search(r'ASSISTANT:\s*(.*)', outputs[0]["generated_text"])
    if match:
        # Wrap the text to fit within 80 characters per line
        return textwrap.fill(match.group(1), width=80)
    else:
        return "No description found."

# Function to query an image
def query_image(image_path, query):
    image = Image.open(image_path)
    prompt_instructions = """
    Respond to the following image query with as much detail as possible:
    """ + query
    prompt = "USER: <image>\n" + prompt_instructions + "\nASSISTANT:"
    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # Extract the response text
    match = re.search(r'ASSISTANT:\s*(.*)', outputs[0]["generated_text"])
    if match:
        # Wrap the text to fit within 80 characters per line
        return textwrap.fill(match.group(1), width=80)
    else:
        return "No response found."

# Example usage
image_path = "/content/HOME.jpg"  # Replace with your image path
description = describe_image(image_path)
print("Image Description:", description)

query = "Is the image related to a movie, if so, what's the movie about?"
query_response = query_image(image_path, query)
print("Image Query Response:", query_response)

