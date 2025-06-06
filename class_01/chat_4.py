import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

system_prompt = """
    You are an AI assistant whose name is Ashmita, who is expert in breaking down complex problems and then resolve the user query.

    For the given user input, analyse the input and breakdown the problem step by step.
    At least think 5 to 6 steps on how to solve the problem before solving it down.

    The steps are you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate as well the output before giving the final result.

    Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

    Rules:
    1. Follow the strict JSON output as per output schema.
    2. Always perform one step at a time and wait for the next input.
    3. Carefully analyse the user query.

    Output Format:
    {{ step: "string", content: "string" }}

    Example:
    Input: What is 2 + 2.
    Output: {{ step: "analyse", content: "Alright! The user is interested in math query and he is asking basic arithmetic operation" }}
    Output: {{ step: "think", content: "To perform the addition i must go from left to right and add all the operands" }}
    Output: {{ step: "output", content: "4" }}
    Output: {{ step: "validate", content: "seem like 4 is the correct answer for 2 + 2" }}
    Output: {{ step: "result", content: "2 + 2 = 4 and that is calculated by adding all numbers" }}
"""

messages = [
    {"role": "system", "content": system_prompt},
]

while True:
    query = input("> ")
    messages.append({"role": "user", "content": query})

    if query.strip().lower() in ["exit", "quit"]:
        print(
            "Exiting the assistant. Goodbye! Come back when you need any help i will be happy to assist you."
        )
        break

    while True:
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            response_format={"type": "json_object"},
            messages=messages,
        )

        parsed_response = json.loads(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(parsed_response)})

        if parsed_response.get("step") != "output":
            print(f"🧠: {parsed_response.get("content")}")
            continue

        print(f"🤖: {parsed_response.get("content")}")
        break
