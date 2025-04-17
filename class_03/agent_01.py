import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# gemini_api_key = os.getenv("GEMINI_API_KEY")

# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY is not set")

# client = OpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def query_db(sql):
    pass


def run_command(command):
    result = os.system(command=command)
    return result


def get_weather(city: str):
    # TODO: Do an actual API call
    # return "31 degree celcius"

    print(f"⛏️: Tool Called: get_weather", city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather is {city} is {response.text}"
    return "Something went wrong"


def add(x, y):
    print(f"⛏️: Tool Called: add", x, y)
    return x + y


available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as a input and returns the current weather for the city",
    },
    "add": {
        "fn": add,
        "description": "Takes two numbers x and y and return their sum of the given numbers",
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns output",
    },
}

system_prompt = """
    You are a helpful AI assistant who is specialized in resolving user query.
    You work on start, analyse, action and observe mode.
    For the give user query and available tools, plan the step by step execution based on the planning, select the relevant tool from the available tool and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON format.
    - Always perform one set at a time and wait for the next input.
    - Carefully analyse the user query.

    Output JSON format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - get_weather: Takes a city name as an input and returns the current weather for the city
    - run_command: Takes a command as input to execute on system and returns output

    Example:
    User Query: What is the weather of the new york?
    Output: {{ "step": "plan", "content": "The user is interested in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Celcius" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees" }}
"""

messages = [{"role": "system", "content": system_prompt}]

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
            model="gpt-4.1-mini-2025-04-14",
            response_format={"type": "json_object"},
            messages=messages,
        )

        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(parsed_output)})

        if parsed_output.get("step") == "plan":
            print(f"🧠: {parsed_output.get("content")}")
            continue

        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if available_tools.get(tool_name, False) != False:
                output = available_tools[tool_name].get("fn")(tool_input)
                messages.append(
                    {
                        "role": "assistant",
                        "content": json.dumps({"step": "observe", "output": output}),
                    }
                )
                continue

        if parsed_output.get("step") == "output":
            print(f"🤖: {parsed_output.get("content")}")
            break
