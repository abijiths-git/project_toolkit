import os
import shutil
from collections import defaultdict
import traceback

try:
    # Get current working directory and script filename
    folder_path = os.getcwd()
    script_filename = os.path.basename(__file__)

    # Group files by base name (excluding the script itself)
    file_groups = defaultdict(list)
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if os.path.isfile(full_path) and filename != script_filename:
            base_name = os.path.splitext(filename)[0]
            file_groups[base_name].append(filename)

    if not file_groups:
        print("No files found to group.")
    else:
        # Create folders and move files
        for base_name, files in file_groups.items():
            folder_name = os.path.join(folder_path, base_name)

            # Create folder if it doesn't exist
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            for file in files:
                src = os.path.join(folder_path, file)
                dest = os.path.join(folder_name, file)
                try:
                    shutil.move(src, dest)
                    print(f"Moved: {file} → {base_name}/")
                except Exception as move_error:
                    print(f"Failed to move {file}: {move_error}")

        print(f"\n✅ Grouping completed in: {folder_path}")

except Exception as e:
    print("❌ An error occurred:")
    print(traceback.format_exc())

input("\nPress Enter to exit...")  # Keeps the CMD window open
