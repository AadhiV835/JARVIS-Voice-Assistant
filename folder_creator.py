import os
import subprocess
def create_project_folder(folder_name):
    try:
        path = os.path.join("project_files", folder_name)
        os.makedirs(path)
        print(f"Folder created at {path}")
        subprocess.run(["explorer", path])
    except FileExistsError:
        print("The folder already exists.")
    except Exception as e:
        print(f"Error creating folder: {e}")
