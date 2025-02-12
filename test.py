import requests
import os
from dotenv import load_dotenv

load_dotenv()

HUGGING_FACE_API_KEY = os.getenv("HF_API_KEY")
MODEL_NAME = "HuggingFaceH4/zephyr-7b-alpha"

def test_zephyr(prompt):
    API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
    
    payload = {
        "inputs": prompt,
        "parameters": {"max_length": 500, "temperature": 0.8, "top_p": 0.9, "do_sample": True}
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    print("Zephyr Response:", response.json())

test_zephyr("Why is a career in social sciences suitable for a person with a phlegmatic and sanguine temperament?")