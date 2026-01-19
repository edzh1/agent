import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        wd_full_path = os.path.abspath(working_directory)
        file_full_path = os.path.normpath(os.path.join(wd_full_path, file_path))
        if not os.path.commonpath([wd_full_path, file_full_path]) == wd_full_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(file_full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return f"Error: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get file content truncated to 1000 symbols",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)