import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        wd_full_path = os.path.abspath(working_directory)
        file_full_path = os.path.normpath(os.path.join(wd_full_path, file_path))
        if not os.path.commonpath([wd_full_path, file_full_path]) == wd_full_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", file_full_path]
        if args is not None and type(args).__name__ == "list":
            command.extend(args)
        
        completed_process = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, timeout=30)

        output = ""
        if completed_process.returncode != 0:
            output += f"Process exited with code {completed_process.returncode}"
        elif (len(completed_process.stdout) == 0) and (len(completed_process.stderr) == 0):
            output += "No output produced"
        else:
            output += f"STDOUT: {completed_process.stdout}"
            output += f"STDERR: {completed_process.stderr}"

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python file relative to working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to list files from, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments array for python run",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Argument for python run",
                ),
            ),
        },
    ),
)