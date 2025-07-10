from PIL import Image
import os

# Function to resize the image to 500x500
def resize_image(image_path, size=(500, 500)):
    try:
        with Image.open(image_path) as img:
            # Resize the image
            img_resized = img.resize(size)
            # Save the resized image to the same location with the same name
            img_resized.save(image_path)
            print(f"Image has been resized and saved as {image_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

# Automatically get all image files in the specified directory
def get_image_files(directory):
    # Extensions to consider for images
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    # Get all files in the directory and filter image files based on extensions
    return [f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in valid_extensions]

# Example usage:
current_directory = os.getcwd()  # Get current working directory
image_files = get_image_files(current_directory)  # Get image files in the folder

# Loop through each image file in the directory and resize it
for image_file in image_files:
    image_path = os.path.join(current_directory, image_file)

    # Resize and save the image in the same location with the same name
    resize_image(image_path)
