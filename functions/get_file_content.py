import os
from google.genai import types

from .config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        abs_work = os.path.abspath(working_directory)
        abs_target = os.path.abspath(os.path.join(working_directory, file_path))

        if not (abs_target == abs_work or abs_target.startswith(abs_work + os.sep)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Now we're okay to build the tool.
        if not os.path.isfile(abs_target):
            return f'Error: File not found or is not a regular file: "{file_path}"'


        with open(abs_target, "r") as f:
            file_content_string = f.read()
            if len(file_content_string) > MAX_CHARS:
                file_content_string = file_content_string[:MAX_CHARS]
                file_content_string = "\n".join([file_content_string, f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'])

        return file_content_string


    except Exception as e:
        return f'Error: {e}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f'Read a file in the specified directory up to {MAX_CHARS}, constrained to the working directory.',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to read a file from, relative to the working directory. If not provided, find the file in the current working directory.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read, relative to the working directory. If not provided, don't do anything.",
            ),
        },
    ),
)
