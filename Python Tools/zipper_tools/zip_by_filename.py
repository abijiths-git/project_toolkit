import os
import zipfile
from collections import defaultdict
import traceback

try:
    # Get the current folder path and script file name
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
        print("No files found to zip.")
    else:
        # Create zip files with base name only
        for base_name, files in file_groups.items():
            zip_filename = os.path.join(folder_path, f"{base_name}.zip")
            
            # Skip if zip already exists
            if os.path.exists(zip_filename):
                print(f"Skipped: {zip_filename} already exists.")
                continue

            try:
                with zipfile.ZipFile(zip_filename, 'w') as zipf:
                    for file in files:
                        file_path = os.path.join(folder_path, file)
                        zipf.write(file_path, arcname=file)
                        print(f"Added {file} to {base_name}.zip")
                print(f"✔️ Created: {base_name}.zip")
            except Exception as zip_error:
                print(f"❌ Error creating {base_name}.zip: {zip_error}")

    print(f"\n✅ Zipping completed in folder: {folder_path}")

except Exception as e:
    print("❌ An unexpected error occurred:")
    print(traceback.format_exc())

input("\nPress Enter to exit...")  # Keeps the CMD window open on double-click
