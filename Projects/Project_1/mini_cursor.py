import json
import requests
import subprocess
import os
import sys
import shlex
from typing import Dict, Any, List, Optional, Union, Callable
from datetime import datetime
import traceback
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console


console = Console()

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    console.print(
        "[bold red]Error: OPENAI_API_KEY not found in environment variables or .env file[/bold red]"
    )
    sys.exit(1)

client = OpenAI(api_key=api_key)


class AgentMemory:
    def __init__(self, max_history: int = 10):
        self.conversation_history = []
        self.max_history = max_history
        self.working_directory = os.getcwd()
        self.environment_vars = {}
        self.last_command_result = None

    def add_interaction(self, user_query: str, agent_response: str):
        self.conversation_history.append({"user": user_query, "agent": agent_response})
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)

    def get_recent_history(self) -> List[Dict[str, str]]:
        return self.conversation_history[-5:] if self.conversation_history else []

    def update_working_directory(self, new_dir: str):
        self.working_directory = new_dir
        os.chdir(new_dir)

    def set_env_var(self, key: str, value: str):
        self.environment_vars[key] = value
        os.environ[key] = value

    def to_context_dict(self) -> Dict:
        return {
            "working_directory": self.working_directory,
            "environment_vars": self.environment_vars,
            "recent_history": self.get_recent_history(),
            "last_command_result": self.last_command_result,
        }


memory = AgentMemory()


def run_command(command: str) -> str:
    """Execute a shell command and return its output"""
    try:

        args = shlex.split(command)

        if args[0].lower() == "cd":
            try:
                new_dir = args[1] if len(args) > 1 else os.path.expanduser("~")
                memory.update_working_directory(os.path.abspath(new_dir))
                return f"Changed directory to {memory.working_directory}"
            except Exception as e:
                return f"Error changing directory: {str(e)}"

        result = subprocess.run(
            command,
            shell=True,
            cwd=memory.working_directory,
            capture_output=True,
            text=True,
        )

        output = result.stdout
        error = result.stderr

        if result.returncode != 0:
            if error:
                memory.last_command_result = error
                return f"Command failed with error: {error}"
            else:
                memory.last_command_result = "Command failed with no error output"
                return "Command failed with no error output"

        memory.last_command_result = output
        return output if output else "Command executed successfully with no output"

    except Exception as e:
        memory.last_command_result = f"Error executing command: {str(e)}"
        return f"Error executing command: {str(e)}"


def get_file_content(file_path: str) -> str:
    """Read and return the contents of a file"""
    try:

        if not os.path.isabs(file_path):
            file_path = os.path.join(memory.working_directory, file_path)

        with open(file_path, "r") as file:
            content = file.read()
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"


def write_file(path: str, content: str) -> str:
    """Write content to a file"""
    try:

        if not os.path.isabs(path):
            path = os.path.join(memory.working_directory, path)
            print(f"Attempting to write to {path}")
            print(f"memory.working_directory = {memory.working_directory}")

        with open(path, "w") as file:
            file.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing to file: {str(e)}"


def list_directory(dir_path: Optional[str] = None) -> str:
    """List the contents of a directory"""
    try:

        if not dir_path:
            dir_path = memory.working_directory
        elif not os.path.isabs(dir_path):
            dir_path = os.path.join(memory.working_directory, dir_path)

        items = os.listdir(dir_path)
        files = []
        dirs = []

        for item in items:
            full_path = os.path.join(dir_path, item)
            if os.path.isdir(full_path):
                dirs.append(f"{item}/")
            else:
                files.append(item)

        result = (
            "Directories:\n"
            + "\n".join(sorted(dirs))
            + "\n\nFiles:\n"
            + "\n".join(sorted(files))
        )
        return result
    except Exception as e:
        return f"Error listing directory: {str(e)}"


def get_weather(city: str) -> str:
    """Get the current weather for a city"""
    console.print(f"🔨 Tool Called: get_weather for {city}")

    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return f"The weather in {city} is {response.text}."
        return f"Failed to get weather. Status code: {response.status_code}"
    except Exception as e:
        return f"Error getting weather: {str(e)}"


def get_current_datetime() -> str:
    """Get the current date and time"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def search_files(query: str, path: Optional[str] = None) -> str:
    """Search for files containing the query text"""
    if not path:
        path = memory.working_directory

    try:
        result = subprocess.run(
            f"grep -r '{query}' {path} 2>/dev/null || echo 'No matches found'",
            shell=True,
            capture_output=True,
            text=True,
        )
        return result.stdout if result.stdout else "No matches found"
    except Exception as e:
        return f"Error searching files: {str(e)}"


available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as input and returns the current weather for that city.",
    },
    "run_command": {
        "fn": run_command,
        "description": "Executes a terminal command and returns its output. Use for any general command-line operations.",
    },
    "get_file_content": {
        "fn": get_file_content,
        "description": "Reads and returns the content of a file at the specified path.",
    },
    "write_file": {
        "fn": write_file,
        "description": "Writes the provided content to a file at the specified path.",
    },
    "list_directory": {
        "fn": list_directory,
        "description": "Lists the contents of the specified directory or current directory if none provided.",
    },
    "get_current_datetime": {
        "fn": get_current_datetime,
        "description": "Returns the current date and time.",
    },
    "search_files": {
        "fn": search_files,
        "description": "Searches for files containing the specified text within the given directory path.",
    },
}

tool_descriptions = "\n".join(
    [f"- {name}: {tool['description']}" for name, tool in available_tools.items()]
)

system_prompt = f"""
You are an advanced AI Terminal Agent that helps users interact with their computer through natural language.
You work in a start, plan, action, observe mode to handle user queries effectively.

For each user query:
1. Analyze what the user wants
2. Plan the necessary steps to accomplish the task
3. Choose and execute appropriate tools through actions
4. Observe results and respond accordingly

Rules:
- Follow the Output JSON Format precisely
- Perform one step at a time and wait for the next input
- Carefully analyze the user query to understand intent
- Be concise and helpful in your responses
- Use the most appropriate tool for each task
- If necessary, break down complex tasks into multiple steps
- Clearly explain what you're doing at each step
- When using run_command, prefer standard terminal commands

Current Working Directory: {memory.working_directory}

Available Tools:
{tool_descriptions}

Output JSON Format:
{{
    "step": "string",  // One of: "plan", "action", "observe", "output"
    "content": "string",  // Description of current step or final response
    "function": "string",  // Name of function if step is "action"
    "input": "string" or object  // Input parameters for the function
}}

Example Flow:
User Query: "What files are in my current directory and what's the weather in New York?"
Output: {{ "step": "plan", "content": "I'll list the files in the current directory and then check the weather for New York." }}
Output: {{ "step": "plan", "content": "First, I'll use list_directory to see the files." }}
Output: {{ "step": "action", "function": "list_directory", "input": null }}
Output: {{ "step": "observe", "content": "Directories: ... Files: ..." }}
Output: {{ "step": "plan", "content": "Now I'll check the weather in New York." }}
Output: {{ "step": "action", "function": "get_weather", "input": "New York" }}
Output: {{ "step": "observe", "content": "The weather in New York is..." }}
Output: {{ "step": "output", "content": "Here are the files in your current directory: [file list]. The weather in New York is currently [weather details]." }}
"""


def run_agent():
    print("AI Terminal Agent\nType 'exit' or 'quit' to end the session.")

    messages = [{"role": "system", "content": system_prompt}]

    while True:
        user_query = input("> ")

        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_query})

        print("Processing...")

        final_response = None
        while final_response is None:
            try:
                response = client.chat.completions.create(
                    model="gpt-4.1-mini-2025-04-14",
                    response_format={"type": "json_object"},
                    messages=messages,
                )

                try:
                    parsed_output = json.loads(response.choices[0].message.content)
                    messages.append(
                        {"role": "assistant", "content": json.dumps(parsed_output)}
                    )
                except json.JSONDecodeError:
                    print("Error parsing JSON response from AI")
                    print(f"Raw response: {response.choices[0].message.content}")
                    break

                if parsed_output.get("step") == "plan":
                    print(f"🧠 {parsed_output.get('content', 'Planning...')}")
                    continue

                elif parsed_output.get("step") == "action":
                    tool_name = parsed_output.get("function")
                    tool_input = parsed_output.get("input")

                    print(f"🔧 Executing: {tool_name}")

                    if tool_name in available_tools:
                        try:
                            if tool_input is None:
                                output = available_tools[tool_name]["fn"]()
                            elif isinstance(tool_input, dict):
                                output = available_tools[tool_name]["fn"](**tool_input)
                            else:
                                output = available_tools[tool_name]["fn"](tool_input)

                            messages.append(
                                {
                                    "role": "assistant",
                                    "content": json.dumps(
                                        {"step": "observe", "content": output}
                                    ),
                                }
                            )
                        except Exception as e:
                            error_msg = f"Error executing {tool_name}: {str(e)}\n{traceback.format_exc()}"
                            messages.append(
                                {
                                    "role": "assistant",
                                    "content": json.dumps(
                                        {"step": "observe", "content": error_msg}
                                    ),
                                }
                            )
                    else:
                        error_msg = f"Unknown tool: {tool_name}"
                        messages.append(
                            {
                                "role": "assistant",
                                "content": json.dumps(
                                    {"step": "observe", "content": error_msg}
                                ),
                            }
                        )
                    continue

                elif parsed_output.get("step") == "output":
                    final_response = parsed_output.get("content", "No output provided.")

                    memory.add_interaction(user_query, final_response)

            except Exception as e:
                print(f"Error: {str(e)}")
                final_response = f"An error occurred: {str(e)}"

        if final_response:
            print("\n🤖 Response:")
            print(final_response)
            print()


if __name__ == "__main__":
    try:
        run_agent()
    except KeyboardInterrupt:
        print("\nSession terminated by user. Goodbye!")
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        traceback.print_exc()
