import os
import zipfile
from collections import defaultdict

# Get the current folder path and script file name
folder_path = os.getcwd()
script_filename = os.path.basename(__file__)

# Group files by base name (excluding the script itself)
file_groups = defaultdict(list)
for filename in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, filename)) and filename != script_filename:
        base_name = os.path.splitext(filename)[0]
        file_groups[base_name].append(filename)

# Create zip files with base name only
for base_name, files in file_groups.items():
    zip_filename = os.path.join(folder_path, f"{base_name}.zip")
    
    # Skip if zip file already exists
    if os.path.exists(zip_filename):
        continue

    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files:
            file_path = os.path.join(folder_path, file)
            zipf.write(file_path, arcname=file)

print(f"Zipping completed in folder: {folder_path}")
