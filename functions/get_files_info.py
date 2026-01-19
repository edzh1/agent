import os
from google.genai import types

def get_files_info(working_directory, directory="."):
   try:
      abs_path = os.path.abspath(working_directory)
      full_path = os.path.normpath(os.path.join(abs_path, directory))

      if not os.path.commonpath([abs_path, full_path]) == abs_path:
         return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
      if not os.path.isdir(full_path):
         return f'Error: "{directory}" is not a directory'
      
      content = os.listdir(full_path)
      data = []
      for item in content:
         try:
            data.append(f"- {item}: file_size={os.path.getsize(os.path.join(full_path, item))} bytes, is_dir={not os.path.isfile(os.path.join(full_path, item))}")
         except (OSError, FileNotFoundError) as e:
            continue 
   except Exception as e:
      return f"Error: {e}"      

   return "\n".join(data)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)