import os

def create_folder(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def get_file_full_name(file_path, file_name):
    return os.path.join(file_path, file_name)