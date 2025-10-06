import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        abs_work = os.path.abspath(working_directory)
        abs_target = os.path.abspath(os.path.join(working_directory, directory))

        if not (abs_target == abs_work or abs_target.startswith(abs_work + os.sep)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Now we're okay to build the tool.
        if not os.path.isdir(abs_target):
            return f'Error: "{directory}" is not a directory'

        lines = []
        for name in os.listdir(abs_target):
            full = os.path.join(abs_target, name)
            is_dir = os.path.isdir(full)
            size = os.path.getsize(full)
            lines.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(lines)

    except Exception as e:
        return f'Error: {e}'

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="List files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, list files in the working directory itself.",
            ),
        },
    ),
)
