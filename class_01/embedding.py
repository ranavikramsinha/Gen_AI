import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

text = "The cat sat on the mat"

response = client.embeddings.create(
    input=text,
    model="models/text-embedding-004",
)

print("Vector Embeddings:", response.data[0].embedding)