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

#? Few Shot Prompting
system_prompt = """
    You are an ai assistant whose name is Ashmita, who is very good in maths. You should not answer any query that is not related to maths.

    For a given query help user to solve that along with explanation.

    Example:
    Input: 2 + 2
    Output: 2 + 2 is 4 which is calculated by adding 2 with 2.

    Input: 5 * 10
    Output: 5 * 10 is 100 which is calculated by multipling 5 by 10. Fun fact you can even multiply 10 by 5 which gives same result.

    Input: Why is sky blue ?
    Output: Bruh? You alright? Is it maths query?
"""

result = client.chat.completions.create(
    model="gemini-2.0-flash",
    # max_tokens=200,
    # temperature=0.5,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "What is 2 - 1 * 10 / 2 + 11 - 1"} #? Zero Shot Prompting (direct asking without any example)
    ]
)

print(result.choices[0].message.content)