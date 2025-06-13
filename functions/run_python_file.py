import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_dir.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_dir):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        content = subprocess.run(['python3', abs_dir], timeout=30, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, cwd=abs_working_dir)
        if content.stdout == '' and content.stderr == '':
            return 'No output produced.'
        output_str = ''
        output_str += f'STDOUT:{content.stdout}\n'
        output_str += f'STDERR:{content.stderr}\n'
        if content.returncode != 0:
            output_str += f'Process exited with code {content.returncode}'
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    return output_str.rstrip()