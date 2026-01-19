import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        wd_full_path = os.path.abspath(working_directory)
        file_full_path = os.path.normpath(os.path.join(wd_full_path, file_path))
        if not os.path.commonpath([wd_full_path, file_full_path]) == wd_full_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(file_full_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(file_full_path), exist_ok=True)
        with open(file_full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file relative to working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to list files from, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content for a file to be written",
            ),
        },
    ),
)