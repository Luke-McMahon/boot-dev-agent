import os

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
