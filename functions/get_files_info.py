import os

def get_files_info(working_directory, directory=None):
    abs_working_dir = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory, directory))
    if not abs_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_dir):
        return f'Error: "{directory}" is not a directory'
    try:
        scan = os.scandir(abs_dir)
        contents = ''
        for item in scan:
            contents += f'- {item.name}: file_size={os.stat(item.path).st_size} bytes, is_dir={item.is_dir()}\n'
    except Exception as e:
        return f'Error: {e}'
    
    return contents.rstrip()