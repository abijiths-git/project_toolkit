import os

def rename_files_to_lowercase():
    # Get the current working directory
    current_dir = os.getcwd()
    print(f"Scanning directory: {current_dir}")

    for filename in os.listdir(current_dir):
        file_path = os.path.join(current_dir, filename)

        # Ignore directories
        if os.path.isfile(file_path):
            # Create lowercase version of the filename
            new_name = filename.lower()
            new_path = os.path.join(current_dir, new_name)

            # Only rename if the new name is different
            if filename != new_name:
                try:
                    os.rename(file_path, new_path)
                    print(f"Renamed: {filename} → {new_name}")
                except Exception as e:
                    print(f"Error renaming {filename}: {e}")

if __name__ == "__main__":
    rename_files_to_lowercase()
