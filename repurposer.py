import os
import random
from PIL import Image, ImageEnhance
import piexif
import hashlib


def generate_random_name():
    return f"IMG_{random.randint(1000, 1500)}"


def apply_random_transformations(image):
    try:
        # Random resolution change (increase or decrease)
        # Random integer between 80 and 120
        resolution_factor = random.randint(80, 120) / 100
        new_width = int(image.width * resolution_factor)
        new_height = int(image.height * resolution_factor)
        image = image.resize((new_width, new_height))

        # Random brightness change
        # Random integer between 80 and 120
        brightness_factor = random.randint(80, 120) / 100
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness_factor)

        # Random contrast change
        # Random integer between 80 and 120
        contrast_factor = random.randint(80, 120) / 100
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast_factor)

        # Random color (saturation) change
        # Random integer between 80 and 120
        saturation_factor = random.randint(80, 120) / 100
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(saturation_factor)

        # Random sharpness change
        # Random integer between 80 and 120
        sharpness_factor = random.randint(80, 120) / 100
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(sharpness_factor)

        # Random DPI change (if it exists)
        if "dpi" in image.info:
            # Random integer between 80 and 120
            dpi_factor = random.randint(80, 120) / 100
            dpi_x, dpi_y = image.info["dpi"]
            image.info["dpi"] = (
                int(dpi_x * dpi_factor),
                int(dpi_y * dpi_factor),
            )

        return image
    except Exception as e:
        print(f"Error applying random transformations: {e}")
        return image


def process_image(input_image_path):
    try:
        # Preprocess and convert the image to RGB
        img = Image.open(input_image_path).convert("RGB")

        # Apply random transformations
        img = apply_random_transformations(img)

        # Save the modified image with a random name
        new_name = generate_random_name()
        img.save(os.path.join(output_directory, f"{new_name}.jpg"))

        # Change metadata and MD5 hash for the processed image
        change_metadata(os.path.join(output_directory,
                        f"{new_name}.jpg"), new_name)
        change_md5(os.path.join(output_directory, f"{new_name}.jpg"))

        return new_name
    except Exception as e:
        print(f"Error processing {input_image_path}: {e}")
        return None


def change_metadata(image_path, new_name):
    try:
        exif_dict = piexif.load(image_path)
        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = new_name.encode(
            "utf-8")
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image_path)
    except Exception as e:
        print(f"Error changing metadata for {image_path}: {e}")


def change_md5(image_path):
    try:
        with open(image_path, 'rb') as f:
            data = f.read()
        new_md5 = hashlib.md5(data).hexdigest()
        new_data = data.replace(b'MD5=', f'MD5={new_md5}'.encode())
        with open(image_path, 'wb') as f:
            f.write(new_data)
    except Exception as e:
        print(f"Error changing MD5 for {image_path}: {e}")


if __name__ == "__main__":
    num_folders = int(input("Enter the number of folders to create: "))
    total_cleaned = 0  # Initialize the total number of cleaned images

    for folder_index in range(1, num_folders + 1):
        output_directory = f"output {folder_index}"

        # Create a directory for the modified images
        os.makedirs(output_directory, exist_ok=True)

        input_directory = "./input"

        # Process and modify images
        image_files = [f for f in os.listdir(input_directory) if f.lower().endswith(
            ('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]

        for image_file in image_files:
            input_image_path = os.path.join(input_directory, image_file)
            process_image(input_image_path)
            total_cleaned += 1  # Increment the total cleaned count

    print(f"{total_cleaned} images cleaned")
