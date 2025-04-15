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

result = client.chat.completions.create(
    model="gemini-2.0-flash",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "What is 5 * 5 + 75"},
        # ?
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "step": "analyse",
                    "content": "The user is asking to solve an arithmetic expression involving multiplication and addition.",
                }
            ),
        },
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "step": "think",
                    "content": "To solve this, I need to follow the order of operations (PEMDAS/BODMAS), which means performing the multiplication first, and then the addition.",
                }
            ),
        },
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "step": "output",
                    "content": "First, calculate 5 * 5, which equals 25.  Then, add 25 to 75.  25 + 75 = 100.",
                }
            ),
        },
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "step": "validate",
                    "content": "The calculation 5 * 5 = 25 is correct.  And 25 + 75 = 100 is also correct. Thus, the final answer should be 100",
                }
            ),
        },
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "step": "result",
                    "content": "5 * 5 + 75 = 100, calculated by first multiplying 5 and 5, and then adding the result to 75.",
                }
            ),
        },
    ],
)

print(result.choices[0].message.content)
