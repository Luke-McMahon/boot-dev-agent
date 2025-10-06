import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_content import schema_get_file_content, get_file_content
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file


load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

name_to_function = {
        'get_files_info': get_files_info,
        'get_file_content': get_file_content,
        'run_python_file': run_python_file,
        'write_file': write_file
}

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    function_name = function_call_part.name
    func = name_to_function.get(function_name)
    if not func:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"}
                )
            ]
        )

    kwargs = dict(function_call_part.args)
    kwargs["working_directory"] = "./calculator"
    function_result = func(**kwargs)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result}
            )
        ]
    )

def main():
    if len(sys.argv) < 2:
        print("You must provide a query.")
        sys.exit(1)

    user_prompt = sys.argv[1]
    verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    resp = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
        ),
    )

    if verbose:
        prompt_tokens = resp.usage_metadata.prompt_token_count
        response_tokens = resp.usage_metadata.candidates_token_count

        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    if resp.function_calls:
        for function_call_part in resp.function_calls:
            function_call_results = call_function(function_call_part, verbose)
            resp_obj = function_call_results.parts[0].function_response.response
            if resp_obj is None:
                raise Exception(f"{function_call_part.name} failed")

            if verbose:
                print(resp_obj)
            else: 
                if "result" in resp_obj:
                    print(f"-> {resp_obj['result']}")
                elif "error" in resp_obj:
                    print(f"-> {resp_obj['error']}")
                else:
                    raise Exception(f"Unexpected response shape from {function_call_part.name}: {resp_obj}")

    else:
        print(resp.text)


if __name__ == "__main__":
    main()
