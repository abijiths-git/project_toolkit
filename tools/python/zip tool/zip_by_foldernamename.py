import os
import zipfile

# Get the current folder path
folder_path = os.getcwd()

# Iterate through all items in the current directory
for item in os.listdir(folder_path):
    item_path = os.path.join(folder_path, item)

    # Check if the item is a directory
    if os.path.isdir(item_path):
        zip_filename = os.path.join(folder_path, f"{item}.zip")

        # Skip if zip file already exists
        if os.path.exists(zip_filename):
            continue

        # Create the zip file
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(item_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Save relative path in archive
                    arcname = os.path.relpath(file_path, start=folder_path)
                    zipf.write(file_path, arcname=arcname)

print(f"Zipping completed for folders in: {folder_path}")
