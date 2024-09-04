import os
import json
from openai import OpenAI
import importlib

# Get the directory of the current file (openai_api.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the tools from the tools.json file using the absolute path
tools_path = os.path.join(current_dir, 'tools.json')
with open(tools_path) as f:
    tools = json.load(f)

def dynamic_import_function(function_name):
    # Import the function dynamically from functions.py
    module = importlib.import_module("openai_util.functions")
    return getattr(module, function_name)

def execute_function_call(tool_call):
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    
    # Dynamically import and execute the function
    func = dynamic_import_function(function_name)
    return func(**arguments)

def prompt(messages):
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    # First call to OpenAI API to detect tool calls
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        max_tokens=2000
    )

    generated_answer = "No response generated"
    if response.choices:
        choice = response.choices[0]
        if hasattr(choice.message, 'tool_calls') and choice.message.tool_calls:
            tool_calls = choice.message.tool_calls
            print("Tool calls: ", tool_calls)
            tool_responses = []
            for tool_call in tool_calls:
                function_result = execute_function_call(tool_call)
                if function_result:
                    tool_responses.append({
                        "role": "tool",
                        "content": json.dumps(function_result),
                        "tool_call_id": tool_call.id
                    })
            
            # Prepare the chat completion call payload with the function call results
            completion_payload = {
                "model": "gpt-4o-mini",
                "messages": messages + [choice.message] + tool_responses
            }

            print("Completion payload: ", completion_payload)

            # Second call to OpenAI API with the function call results
            final_response = client.chat.completions.create(
                model=completion_payload["model"],
                messages=completion_payload["messages"],
                max_tokens=2000
            )

            if final_response.choices:
                final_choice = final_response.choices[0]
                if final_choice.message.content:
                    generated_answer = final_choice.message.content.strip()
        else:
            if choice.message.content:
                generated_answer = choice.message.content.strip()

    messages.append({"role": "assistant", "content": generated_answer})
    return generated_answer, messages