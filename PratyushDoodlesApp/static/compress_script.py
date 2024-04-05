import os
from PIL import Image

def reduce_image_quality(input_path, quality_percentage):
    """
    Reduce the quality of an image by a given percentage and overwrite the original file.

    Args:
    - input_path: Path to the input image file.
    - quality_percentage: Percentage by which to reduce image quality.
    """

    image = Image.open(input_path)
    # Reduce quality by converting the image to JPEG format
    image.save(input_path, quality=quality_percentage)
    image.close()

def resize_image(input_path, new_size):
    """
    Resize an image to a new size and overwrite the original file.

    Args:
    - input_path: Path to the input image file.
    - new_size: Tuple specifying the new width and height for resizing (e.g., (width, height)).
    """
    image = Image.open(input_path)
    # Resize the image
    resized_image = image.resize(new_size)
    resized_image.save(input_path)
    resized_image.close()

def process_directory(directory, quality_percentage, new_size):
    """
    Process a directory and its subdirectories to reduce image quality and resize images.

    Args:
    - directory: Path to the directory to process.
    - quality_percentage: Percentage by which to reduce image quality.
    - new_size: Tuple specifying the new width and height for resizing (e.g., (width, height)).
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is an image
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                input_path = os.path.join(root, file)
                if (os.stat(input_path).st_size/1000) > 100:
                    reduce_image_quality(input_path, quality_percentage)
                    resize_image(input_path, new_size)
                    print(f"Processed {input_path}")

def main():
    directory = input("Enter the directory path: ")
    quality_percentage = int(input("Enter the percentage to reduce image quality (0-100): "))
    new_width = int(input("Enter the new width for resizing: "))
    new_height = int(input("Enter the new height for resizing: "))
    new_size = (new_width, new_height)

    if not os.path.isdir(directory):
        print("Invalid directory path.")
        return

    if quality_percentage < 0 or quality_percentage > 100:
        print("Invalid quality percentage. It should be between 0 and 100.")
        return

    process_directory(directory, quality_percentage, new_size)
    print("Image quality reduction and resizing process completed.")

if __name__ == "__main__":
    main()
