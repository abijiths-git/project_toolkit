import os

def rename_folders_to_lowercase():
    current_dir = os.getcwd()
    print(f"📁 Scanning folders in: {current_dir}\n")

    renamed = 0
    skipped = 0

    for folder_name in os.listdir(current_dir):
        full_path = os.path.join(current_dir, folder_name)
        if os.path.isdir(full_path):
            new_name = folder_name.lower()
            new_path = os.path.join(current_dir, new_name)
            if folder_name != new_name:
                try:
                    os.rename(full_path, new_path)
                    print(f"✔️ Renamed: {folder_name} → {new_name}")
                    renamed += 1
                except Exception as e:
                    print(f"❌ Error renaming {folder_name}: {e}")
            else:
                skipped += 1

    print(f"\n✅ Renamed {renamed} folder(s).")
    if skipped:
        print(f"↪️ Skipped {skipped} folder(s) already lowercase.")

    input("\nPress Enter to exit...")  # Keeps window open on double-click

if __name__ == "__main__":
    rename_folders_to_lowercase()
