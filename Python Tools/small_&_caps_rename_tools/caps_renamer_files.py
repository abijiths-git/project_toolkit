import os
import traceback

def rename_files_to_uppercase():
    current_dir = os.getcwd()
    print(f"📂 Scanning directory: {current_dir}\n")

    renamed = 0
    skipped = 0

    for filename in os.listdir(current_dir):
        file_path = os.path.join(current_dir, filename)

        # Ignore directories
        if os.path.isfile(file_path):
            name, ext = os.path.splitext(filename)

            if any(c.islower() for c in name):
                new_name = name.upper() + ext
                new_path = os.path.join(current_dir, new_name)

                try:
                    os.rename(file_path, new_path)
                    print(f"✔️ Renamed: {filename} → {new_name}")
                    renamed += 1
                except Exception as e:
                    print(f"❌ Error renaming {filename}: {e}")
            else:
                skipped += 1

    if renamed == 0:
        print("ℹ️ No files needed renaming.")
    else:
        print(f"\n✅ Renamed {renamed} file(s).")
    if skipped:
        print(f"↪️ Skipped {skipped} file(s) already uppercase.")

if __name__ == "__main__":
    try:
        rename_files_to_uppercase()
    except Exception:
        print("❌ Unexpected error:")
        print(traceback.format_exc())

    input("\nPress Enter to exit...")  # Keeps CMD window open
