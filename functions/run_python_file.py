import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        commands = ['python3', abs_file_path]
        if args:
            commands.extend(args)
        content = subprocess.run(commands, timeout=30, capture_output=True, text=True, cwd=abs_working_dir)
        output = []
        if content.stdout:
            output.append(f'STDOUT:\n{content.stdout}')
        if content.stderr:
            output.append(f'STDERR:\n{content.stderr}')
        if content.returncode != 0:
            output_str += f'Process exited with code {content.returncode}'
        return '\n'.join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file from the file in the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to run, relative to the working directory.",
            ),
        },
    ),
)