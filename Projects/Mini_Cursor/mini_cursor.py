# import os
# import json
# import requests
# import textwrap
# import subprocess
# from dotenv import load_dotenv
# from openai import OpenAI

# # Load environment variables
# dotenv_loaded = load_dotenv()

# # Initialize OpenAI client
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# # ==================== Tools ====================

# def query_db(sql):
#     pass

# # Run arbitrary shell command
# def run_command(command: str):
#     result = subprocess.run(command, shell=True, capture_output=True, text=True)
#     return result.stdout.strip() or result.stderr.strip()

# # Fetch weather via wttr.in
# def get_weather(city: str):
#     print(f"⛏️: Tool Called: get_weather", city)
#     url = f"https://wttr.in/{city}?format=%C+%t"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return f"The weather for {city} is {response.text}"
#     return "Something went wrong"

# # Simple addition function
# def add(x, y):
#     print(f"⛏️: Tool Called: add", x, y)
#     return x + y

# # Create or overwrite a file with given content
# def create_file(params):
#     print("⛏️: Tool Called: create_file", params)
#     try:
#         data = json.loads(params) if isinstance(params, str) else params
#         filename = data.get("filename")
#         content = data.get("content", "")
#         with open(filename, "w", encoding="utf-8") as f:
#             f.write(content)
#         return f"{filename} created successfully"
#     except Exception as e:
#         return f"Error creating file: {e}"

# # Edit (append or overwrite) a file's content
# def edit_file(params):
#     print("⛏️: Tool Called: edit_file", params)
#     try:
#         data = json.loads(params) if isinstance(params, str) else params
#         filename = data.get("filename")
#         content = data.get("content", "")
#         mode = data.get("mode", "w")  # 'w' replace or 'a' append
#         with open(filename, mode, encoding="utf-8") as f:
#             f.write(content)
#         return f"{filename} edited successfully"
#     except Exception as e:
#         return f"Error editing file: {e}"

# # Run a code file based on its extension (supports multiple languages)
# def run_file(params):
#     print("⛏️: Tool Called: run_file", params)
#     try:
#         data = json.loads(params) if isinstance(params, str) else params
#         filename = data.get("filename")
#         base, ext = os.path.splitext(filename)
#         if ext == ".py":
#             cmd = f"python {filename}"
#         elif ext == ".js":
#             cmd = f"node {filename}"
#         elif ext == ".cpp":
#             exe = f"{base}.out"
#             compile_cmd = f"g++ {filename} -o {exe}"
#             compile_out = run_command(compile_cmd)
#             if compile_out:
#                 return f"Compile error:\n{compile_out}"
#             cmd = exe
#         elif ext == ".c":
#             exe = f"{base}.out"
#             compile_cmd = f"gcc {filename} -o {exe}"
#             compile_out = run_command(compile_cmd)
#             if compile_out:
#                 return f"Compile error:\n{compile_out}"
#             cmd = exe
#         elif ext == ".java":
#             compile_cmd = f"javac {filename}"
#             compile_out = run_command(compile_cmd)
#             if compile_out:
#                 return f"Compile error:\n{compile_out}"
#             cmd = f"java {base}"
#         elif ext == ".go":
#             cmd = f"go run {filename}"
#         elif ext == ".rb":
#             cmd = f"ruby {filename}"
#         elif ext == ".sh":
#             cmd = f"bash {filename}"
#         else:
#             cmd = filename
#         return run_command(cmd)
#     except Exception as e:
#         return f"Error running file: {e}"

# # Specialized tool: create sum.py template (accepts optional params)
# def create_sum_file(params=None):
#     print("⛏️: Tool Called: create_sum_file", params)
#     template = textwrap.dedent('''\
#         def add(x, y):
#             """Return the sum of two numbers."""
#             return x + y

#         if __name__ == "__main__":
#             a = int(input("Enter first number: "))
#             b = int(input("Enter second number: "))
#             print("Sum:", add(a, b))
#     ''')
#     with open("sum.py", "w", encoding="utf-8") as f:
#         f.write(template)
#     return "sum.py created successfully"

# # Git tool: add all, commit with message, and push
# def git_commit_and_push(params):
#     print("⛏️: Tool Called: git_commit_and_push", params)
#     try:
#         data = json.loads(params) if isinstance(params, str) else params
#         message = data.get("message", "")
#         out_add = run_command("git add .")
#         out_commit = run_command(f'git commit -m "{message}"')
#         out_push = run_command("git push")
#         return f"git add output:\n{out_add}\ngit commit output:\n{out_commit}\ngit push output:\n{out_push}"
#     except Exception as e:
#         return f"Error in git_commit_and_push: {e}"

# # ==================== Tool Registry ====================
# available_tools = {
#     "get_weather": {"fn": get_weather, "description": "Fetches weather for a city."},
#     "add": {"fn": add, "description": "Returns sum of two numbers."},
#     "run_command": {"fn": run_command, "description": "Runs a shell command."},
#     "create_file": {"fn": create_file, "description": "Creates a file with specified content."},
#     "edit_file": {"fn": edit_file, "description": "Edits (append/overwrite) a file."},
#     "run_file": {"fn": run_file, "description": "Executes code files (py, js, cpp, c, java, go, rb, sh)."},
#     "create_sum_file": {"fn": create_sum_file, "description": "Creates a sum.py with add function template."},
#     "git_commit_and_push": {"fn": git_commit_and_push, "description": "Stages all changes, commits with message, and pushes to GitHub repo."}
# }

# # ==================== System Prompt ====================
# system_prompt = """
# You are an AI assistant that plans steps and uses tools to fulfill user requests.
# Follow start, analyse, action, observe, output flow with JSON steps.

# Output JSON format:
# {
#   "step": <plan|action|observe|output>,
#   "content": "string",
#   "function": "tool_name if action",
#   "input": "parameters"
# }

# Available tools:
# - create_file
# - edit_file
# - run_file
# - create_sum_file
# - run_command
# - get_weather
# - add
# - git_commit_and_push

# Examples:
# 1) Create any file:
#   plan: User wants example.txt with sample text
#   plan: use create_file
#   action: create_file, input: {"filename":"example.txt","content":"Hello"}
#   observe: example.txt created successfully
#   output: "Created example.txt with provided content."

# 2) Edit a file:
#   plan: User wants to append to example.txt
#   plan: use edit_file
#   action: edit_file, input: {"filename":"example.txt","content":" More text","mode":"a"}
#   observe: example.txt edited successfully
#   output: "Appended to example.txt."

# 3) Create sum.py:
#   plan: use create_sum_file
#   action: create_sum_file
#   observe: sum.py created successfully
#   output: "Created sum.py with addition function."

# 4) Run code files in multiple languages:
#   plan: User wants to run hello.cpp
#   plan: use run_file
#   action: run_file, input: {"filename":"hello.cpp"}
#   observe: <output or compile errors>
#   output: "Here’s the output of hello.cpp."

# 5) Push changes to GitHub:
#   plan: use git_commit_and_push
#   action: git_commit_and_push, input: {"message":"Commit message"}
#   observe: <git outputs>
#   output: "All changes committed and pushed!"
# """

# # Initialize message history
# messages = [{"role": "system", "content": system_prompt}]

# # Main loop
# while True:
#     query = input("> ")
#     messages.append({"role": "user", "content": query})
#     if query.strip().lower() in ["exit", "quit"]:
#         print("Exiting. Goodbye!")
#         break
#     while True:
#         response = client.chat.completions.create(
#             model="gpt-4", messages=messages
#         )
#         parsed = json.loads(response.choices[0].message.content)
#         messages.append({"role":"assistant","content":json.dumps(parsed)})
#         if parsed["step"] == "plan":
#             print(f"🧠: {parsed['content']}")
#             continue
#         if parsed["step"] == "action":
#             tool, inp = parsed["function"], parsed.get("input", "")
#             if tool in available_tools:
#                 out = available_tools[tool]["fn"](inp)
#                 messages.append({"role":"assistant","content":json.dumps({"step":"observe","output":out})})
#                 continue
#         if parsed["step"] == "output":
#             print(f"🤖: {parsed['content']}")
#             break

import os
import json
import requests
import textwrap
import subprocess
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# ==================== Tools ====================

def query_db(sql):
    pass

# Run arbitrary shell command
def run_command(command: str):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip() or result.stderr.strip()

# Fetch weather via wttr.in
def get_weather(city: str):
    print(f"⛏️: Tool Called: get_weather", city)
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather for {city} is {response.text}"
    return "Something went wrong"

# Simple addition function
def add(x, y):
    print(f"⛏️: Tool Called: add", x, y)
    return x + y

# Create or overwrite a file with given content
def create_file(params):
    print("⛏️: Tool Called: create_file", params)
    try:
        data = json.loads(params) if isinstance(params, str) else params
        filename = data.get("filename")
        content = data.get("content", "")
        os.makedirs(os.path.dirname(filename), exist_ok=True) if os.path.dirname(filename) else None
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"{filename} created successfully"
    except Exception as e:
        return f"Error creating file: {e}"

# Edit (append or overwrite) a file's content
def edit_file(params):
    print("⛏️: Tool Called: edit_file", params)
    try:
        data = json.loads(params) if isinstance(params, str) else params
        filename = data.get("filename")
        content = data.get("content", "")
        mode = data.get("mode", "w")  # 'w' replace or 'a' append
        with open(filename, mode, encoding="utf-8") as f:
            f.write(content)
        return f"{filename} edited successfully"
    except Exception as e:
        return f"Error editing file: {e}"

# Run a code file based on its extension
# Supports .py, .js, .cpp, .c, .java, .go, .rb, .sh and generic executables
def run_file(params):
    print("⛏️: Tool Called: run_file", params)
    try:
        data = json.loads(params) if isinstance(params, str) else params
        filename = data.get("filename")
        base, ext = os.path.splitext(filename)
        if ext == ".py":
            cmd = f"python {filename}"
        elif ext == ".js":
            cmd = f"node {filename}"
        elif ext == ".cpp":
            exe = f"{base}.out"
            compile_out = run_command(f"g++ {filename} -o {exe}")
            if compile_out:
                return f"Compile error:\n{compile_out}"
            cmd = exe
        elif ext == ".c":
            exe = f"{base}.out"
            compile_out = run_command(f"gcc {filename} -o {exe}")
            if compile_out:
                return f"Compile error:\n{compile_out}"
            cmd = exe
        elif ext == ".java":
            compile_out = run_command(f"javac {filename}")
            if compile_out:
                return f"Compile error:\n{compile_out}"
            cmd = f"java {base}"
        elif ext == ".go":
            cmd = f"go run {filename}"
        elif ext == ".rb":
            cmd = f"ruby {filename}"
        elif ext == ".sh":
            cmd = f"bash {filename}"
        else:
            cmd = filename
        return run_command(cmd)
    except Exception as e:
        return f"Error running file: {e}"

# Specialized tool: create sum.py template (accepts optional params)
def create_sum_file(params=None):
    print("⛏️: Tool Called: create_sum_file", params)
    template = textwrap.dedent('''\
        def add(x, y):
            """Return the sum of two numbers."""
            return x + y

        if __name__ == "__main__":
            a = int(input("Enter first number: "))
            b = int(input("Enter second number: "))
            print("Sum:", add(a, b))
    ''')
    with open("sum.py", "w", encoding="utf-8") as f:
        f.write(template)
    return "sum.py created successfully"

# Create a basic JS framework starter (React or Vue)
def create_js_framework(params):
    print("⛏️: Tool Called: create_js_framework", params)
    try:
        data = json.loads(params) if isinstance(params, str) else params
        fw = data.get("framework", "react").lower()
        if fw == "react":
            html = textwrap.dedent('''\
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>React App</title>
                </head>
                <body>
                    <div id="root"></div>
                    <script src="index.js" type="module"></script>
                </body>
                </html>
            ''')
            js = textwrap.dedent('''\
                import React from 'react';
                import ReactDOM from 'react-dom';

                function App() {
                    return <h1>Hello React!</h1>;
                }

                ReactDOM.render(<App />, document.getElementById('root'));
            ''')
            pkg = json.dumps({
                "name": "react-app",
                "version": "1.0.0",
                "dependencies": {"react": "^18.0.0", "react-dom": "^18.0.0"},
                "type": "module"
            }, indent=2)
            create_file({"filename": "public/index.html", "content": html})
            create_file({"filename": "src/index.js", "content": js})
            create_file({"filename": "package.json", "content": pkg})
            return "React starter created (public/index.html, src/index.js, package.json)"
        elif fw == "vue":
            html = textwrap.dedent('''\
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Vue App</title>
                    <script src="https://unpkg.com/vue@3"></script>
                </head>
                <body>
                    <div id="app">{{ message }}</div>
                    <script src="app.js"></script>
                </body>
                </html>
            ''')
            js = textwrap.dedent('''\
                const { createApp } = Vue;
                createApp({
                    data() {
                        return { message: 'Hello Vue!' }
                    }
                }).mount('#app');
            ''')
            create_file({"filename": "index.html", "content": html})
            create_file({"filename": "app.js", "content": js})
            return "Vue starter created (index.html, app.js)"
        else:
            return f"Unsupported framework: {fw}. Supported: react, vue."
    except Exception as e:
        return f"Error in create_js_framework: {e}"

# Git tool: add all, commit with message, and push
def git_commit_and_push(params):
    print("⛏️: Tool Called: git_commit_and_push", params)
    try:
        data = json.loads(params) if isinstance(params, str) else params
        message = data.get("message", "")
        out_add = run_command("git add .")
        out_commit = run_command(f'git commit -m "{message}"')
        out_push = run_command("git push")
        return f"git add output:\n{out_add}\ngit commit output:\n{out_commit}\ngit push output:\n{out_push}"
    except Exception as e:
        return f"Error in git_commit_and_push: {e}"

# ==================== Tool Registry ====================
available_tools = {
    "get_weather": {"fn": get_weather},
    "add": {"fn": add},
    "run_command": {"fn": run_command},
    "create_file": {"fn": create_file},
    "edit_file": {"fn": edit_file},
    "run_file": {"fn": run_file},
    "create_sum_file": {"fn": create_sum_file},
    "create_js_framework": {"fn": create_js_framework},
    "git_commit_and_push": {"fn": git_commit_and_push}
}

# ==================== System Prompt ====================
system_prompt = """
You are an AI assistant that plans steps and uses tools to fulfill user requests.
Follow start, analyse, action, observe, output flow with JSON steps.

Output JSON format:
{
  "step": <plan|action|observe|output>,
  "content": "string",
  "function": "tool_name if action",
  "input": "parameters"
}

Available tools:
- create_file
- edit_file
- run_file
- create_sum_file
- create_js_framework
- run_command
- get_weather
- add
- git_commit_and_push

Examples:
1) Create any file:
  plan: use create_file
  action: create_file, input: {"filename":"example.txt","content":"Hello"}
  observe: example.txt created successfully
  output: "Created example.txt with provided content."

2) Create React starter:
  plan: want React project scaffolding
  plan: use create_js_framework
  action: create_js_framework, input: {"framework":"react"}
  observe: React starter created...
  output: "React starter created (public/index.html, src/index.js, package.json)."

3) Create Vue starter:
  plan: want Vue project scaffolding
  plan: use create_js_framework
  action: create_js_framework, input: {"framework":"vue"}
  observe: Vue starter created...
  output: "Vue starter created (index.html, app.js)."

4) Run code files:
  plan: use run_file
  action: run_file, input: {"filename":"script.cpp"}
  observe: <compile/run output>
  output: "Here's the output of script.cpp."

5) Push to GitHub:
  plan: use git_commit_and_push
  action: git_commit_and_push, input: {"message":"Commit message"}
  observe: <git outputs>
  output: "All changes committed and pushed!"
"""

# Initialize message history
messages = [{"role": "system", "content": system_prompt}]

# Main loop
while True:
    query = input("> ")
    messages.append({"role": "user", "content": query})
    if query.strip().lower() in ["exit", "quit"]:
        print("Exiting. Goodbye!")
        break
    while True:
        response = client.chat.completions.create(
            model="gpt-4", messages=messages
        )
        parsed = json.loads(response.choices[0].message.content)
        messages.append({"role":"assistant","content":json.dumps(parsed)})
        if parsed["step"] == "plan":
            print(f"🧠: {parsed['content']}")
            continue
        if parsed["step"] == "action":
            tool, inp = parsed["function"], parsed.get("input", "")
            if tool in available_tools:
                out = available_tools[tool]["fn"](inp)
                messages.append({"role":"assistant","content":json.dumps({"step":"observe","output":out})})
                continue
        if parsed["step"] == "output":
            print(f"🤖: {parsed['content']}")
            break
