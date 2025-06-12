import os

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_dir.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_dir) as file:
            content = file.read(10000)
            if file.read() != '':
                content += f'[...File "{abs_dir}" truncated at 10000 characters]'
    except Exception as e:
        return f'Error: {e}'
    
    return content