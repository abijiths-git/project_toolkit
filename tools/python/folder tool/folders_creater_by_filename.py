import os
import shutil
from collections import defaultdict

# Get current working directory and script filename
folder_path = os.getcwd()
script_filename = os.path.basename(__file__)

# Group files by base name (excluding the script itself)
file_groups = defaultdict(list)
for filename in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, filename)) and filename != script_filename:
        base_name = os.path.splitext(filename)[0]
        file_groups[base_name].append(filename)

# Create folders and move files
for base_name, files in file_groups.items():
    folder_name = os.path.join(folder_path, base_name)

    # Create folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for file in files:
        src = os.path.join(folder_path, file)
        dest = os.path.join(folder_name, file)
        shutil.move(src, dest)

print(f"Grouping completed in folder: {folder_path}")
