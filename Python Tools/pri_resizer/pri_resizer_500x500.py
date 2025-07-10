import os
import sys
import subprocess

# Step 1: Auto-install Pillow if missing
try:
    from PIL import Image
except ImportError:
    print("Pillow not found. Installing it now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    print("Pillow installed. Restart the script.")
    input("Press Enter to exit...")
    sys.exit(1)

# Step 2: Resize Function
def resize_image(image_path, size=(500, 500)):
    try:
        with Image.open(image_path) as img:
            img_resized = img.resize(size)
            img_resized.save(image_path)
            print(f"Resized: {image_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

# Step 3: Get Image Files
def get_image_files(directory):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    return [f for f in os.listdir(directory)
            if os.path.splitext(f)[1].lower() in valid_extensions and os.path.isfile(os.path.join(directory, f))]

# Step 4: Main script logic
def main():
    current_directory = os.getcwd()
    image_files = get_image_files(current_directory)

    if not image_files:
        print("No image files found in the current directory.")
    else:
        print(f"Found {len(image_files)} image(s). Resizing to 500x500...")
        for image_file in image_files:
            image_path = os.path.join(current_directory, image_file)
            resize_image(image_path)

    print("\nDone.")

# Run main
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

    input("\nPress Enter to exit...")  # Keeps window open on double-click
