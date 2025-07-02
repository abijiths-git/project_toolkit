import os
import sys
import subprocess
import importlib.util

# === FUNCTION TO AUTO-INSTALL PACKAGES ===
def ensure_package(package_name):
    try:
        if importlib.util.find_spec(package_name) is None:
            print(f"📦 Installing {package_name} ...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    except Exception as e:
        print(f"❌ Failed to install {package_name}: {e}")
        sys.exit(1)

# Ensure required packages are installed
ensure_package("setuptools")
ensure_package("pandas")
ensure_package("openpyxl")

# Now import them after installing
import pandas as pd
import shutil

# === SETUP PATHS ===
base_dir = os.path.dirname(os.path.abspath(__file__))           # this script's folder
source_folder = os.path.join(base_dir, "images")               # folder containing 5 base images
output_folder = os.path.join(base_dir, "output")               # output folder for renamed copies
excel_file = os.path.join(base_dir, "partnumbers.xlsx")        # Excel file with target part numbers
base_part_number = "1558-ss-8-dgg-l-025"                       # part number used in base image names

# Image suffixes to duplicate
suffixes = ["_iso.png", "_front.png", "_top.png", "_side.png", "_iso_1.png"]

# Create output folder if not exists
os.makedirs(output_folder, exist_ok=True)

# === READ EXCEL FILE ===
try:
    df = pd.read_excel(excel_file)
    part_numbers = df.iloc[:, 0].dropna().astype(str).tolist()
    print(f"🧾 Found {len(part_numbers)} part numbers in Excel.")
except Exception as e:
    print(f"❌ Error reading 'partnumbers.xlsx': {e}")
    sys.exit(1)

# === DUPLICATE AND RENAME IMAGES ===
missing_count = 0
for part in part_numbers:
    for suffix in suffixes:
        src = os.path.join(source_folder, f"{base_part_number}{suffix}")
        dst = os.path.join(output_folder, f"{part}{suffix}")
        if os.path.exists(src):
            shutil.copy(src, dst)
            print(f"✅ Created: {part}{suffix}")
        else:
            print(f"⚠️ Missing base image: {base_part_number}{suffix}")
            missing_count += 1

print("\n🎉 Done! All images processed.")
if missing_count:
    print(f"⚠️ {missing_count} base image(s) were missing and skipped.")
