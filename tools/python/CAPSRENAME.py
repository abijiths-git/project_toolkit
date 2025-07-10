import os

def rename_files_to_uppercase():
    # Get the current working directory
    current_dir = os.getcwd()
    print(f"Scanning directory: {current_dir}")

    for filename in os.listdir(current_dir):
        file_path = os.path.join(current_dir, filename)

        # Ignore directories
        if os.path.isfile(file_path):
            # Split name and extension
            name, ext = os.path.splitext(filename)

            # If name has lowercase letters, rename it
            if any(c.islower() for c in name):
                new_name = name.upper() + ext
                new_path = os.path.join(current_dir, new_name)

                try:
                    os.rename(file_path, new_path)
                    print(f"Renamed: {filename} → {new_name}")
                except Exception as e:
                    print(f"Error renaming {filename}: {e}")

if __name__ == "__main__":
    rename_files_to_uppercase()
