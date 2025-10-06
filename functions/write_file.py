import os
from google.genai import types

from .config import MAX_CHARS

def write_file(working_directory, file_path, content):
    try:
        abs_work = os.path.abspath(working_directory)
        abs_target = os.path.abspath(os.path.join(working_directory, file_path))

        if not (abs_target == abs_work or abs_target.startswith(abs_work + os.sep)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        with open(abs_target, "w") as f:
            file_content_string = f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=f'Write a file in the specified directory, constrained to the working directory. Overwriting existing file if already existing.',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to read a file from, relative to the working directory. If not provided, find the file in the current working directory.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filename to write, relative to the working directory. If not provided, don't do anything.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write. If not provided, don't do anything.",
            ),
        },
    ),
)
