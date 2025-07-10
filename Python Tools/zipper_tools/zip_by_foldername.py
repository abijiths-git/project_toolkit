import os
import zipfile
import traceback

# Get the current folder path
folder_path = os.getcwd()

try:
    folders_zipped = 0
    skipped = 0

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if os.path.isdir(item_path):
            zip_filename = os.path.join(folder_path, f"{item}.zip")

            if os.path.exists(zip_filename):
                print(f"⏭️ Skipped: {zip_filename} already exists.")
                skipped += 1
                continue

            try:
                with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(item_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, start=folder_path)
                            zipf.write(file_path, arcname=arcname)
                print(f"✔️ Zipped: {item} → {item}.zip")
                folders_zipped += 1
            except Exception as zip_err:
                print(f"❌ Error zipping {item}: {zip_err}")

    print(f"\n✅ Completed zipping {folders_zipped} folder(s).")
    if skipped:
        print(f"ℹ️ Skipped {skipped} existing zip(s).")

except Exception as e:
    print("❌ An unexpected error occurred:")
    print(traceback.format_exc())

input("\nPress Enter to exit...")  # Keeps window open after double-click
