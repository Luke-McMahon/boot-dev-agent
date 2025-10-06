import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_work = os.path.abspath(working_directory)
        abs_target = os.path.abspath(os.path.join(working_directory, file_path))

        if not (abs_target == abs_work or abs_target.startswith(abs_work + os.sep)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Now we're okay to build the tool.
        if not os.path.isfile(abs_target):
            return f'Error: File "{file_path}" not found.'

        if not abs_target.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        command = ["python3", file_path]
        if args:
            command.extend(args)
        proc = subprocess.run(command, cwd=abs_work, capture_output=True, timeout=30, text=True)
        out, err = proc.stdout, proc.stderr
        parts = [f"STDOUT:{out}", f"STDERR:{err}"]
        if proc.returncode != 0:
            parts.append(f"Process exited with code {proc.returncode}")

        return "\n".join(parts)
        

    except Exception as e:
        return f'Error: {e}'

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python file, using python3, in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, list files in the working directory itself.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run, relative to the working directory. If not provided, don't do anything.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An array of strings, acting as arguments to be passed to the python file being run. If not provided, just run the file as normal",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)

