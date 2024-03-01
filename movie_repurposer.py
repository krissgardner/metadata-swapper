import os
import random
import moviepy.editor
import moviepy.video.fx.all as vfx
import numpy as np
import colorsys
import hashlib


def generate_random_name():
    return f"VID_{random.randint(1000, 1500)}"

def adjust_contrast(frame, factor):
    """
    Adjust the contrast of an image.
    frame: numpy array representing the image
    factor: contrast adjustment factor
    """
    mean = np.mean(frame, axis=(0, 1))
    return np.clip((frame - mean) * factor + mean, 0, 255).astype(np.uint8)

def adjust_saturation(frame, factor):
    """
    Adjust the color saturation of an image.
    frame: numpy array representing the image (RGB)
    factor: saturation adjustment factor
    """
    # Convert RGB to HSV
    hsv = np.array([[colorsys.rgb_to_hsv(*pixel) for pixel in row] for row in frame / 255.0])

    # Adjust saturation
    hsv[..., 1] = np.clip(hsv[..., 1] * factor, 0, 1)

    # Convert back to RGB
    return np.array([[colorsys.hsv_to_rgb(*pixel) for pixel in row] for row in hsv]) * 255

def apply_random_transformations(clip):
    try:
        # Random resolution change (increase or decrease)
        # Random integer between 80 and 120
        resolution_factor = random.randint(80, 120) / 100
        new_width = int(clip.w * resolution_factor)
        new_height = int(clip.h * resolution_factor)
        clip = clip.resize((new_width, new_height))

        # Random brightness change 
        # Random integer between 80 and 120
        brightness_factor = random.randint(80, 120) / 100
        clip = clip.fx(vfx.colorx, brightness_factor)

        # Random contrast change 
        # Random integer between 80 and 120
        contrast_factor = random.randint(80, 120) / 100
        clip = clip.fl_image(lambda frame: adjust_contrast(frame, contrast_factor))

        # Random saturation change 
        # Random integer between 80 and 120
        # Saturation is very slow for some reason
        # print(f"Saturation")
        # saturation_factor = random.randint(80, 120) / 100
        # clip = clip.fl_image(lambda frame: adjust_saturation(frame, saturation_factor))

        return clip
    except Exception as e:
        print(f"Error applying random transformations: {e}")
        raise e
    
def apply_random_audio_transformations(clip):
    try:
        # Random audio volume
        # Random integer between 80 and 120
        volume_factor = random.uniform(0.8, 1.2)  # Change volume by 20% up or down
        audio = clip.audio.volumex(volume_factor)

        return clip.set_audio(audio)
    except Exception as e:
        print(f"Error applying random audio transformations: {e}")
        raise e
    
def change_md5(path):
    try:
        with open(path, 'rb') as f:
            data = f.read()
        new_md5 = hashlib.md5(data).hexdigest()
        new_data = data.replace(b'MD5=', f'MD5={new_md5}'.encode())
        with open(path, 'wb') as f:
            f.write(new_data)
    except Exception as e:
        print(f"Error changing MD5 for {path}: {e}")
        raise e


def process_video(input_video_file):
    try:
        print(f"Processing {input_video_file}")
        clip = moviepy.editor.VideoFileClip(input_video_file)

        # Apply random transformations
        clip = apply_random_transformations(clip)
        clip = apply_random_audio_transformations(clip)

        # Save the modified video with a random name
        new_name = generate_random_name()
        clip.write_videofile(os.path.join(output_directory, f"{new_name}.mp4"))
        clip.close()

        # Change metadata and MD5 hash for the processed video
        change_md5(os.path.join(output_directory, f"{new_name}.mp4"))
       
    except Exception as e:
        print(f"Error processing {input_video_file}: {e}")
        return None


if __name__ == "__main__":
    num_folders = int(input("Enter the number of folders to create: "))
    total_cleaned = 0  # Initialize the total number of cleaned videos

    # Create a directory for the modified videos
    os.makedirs('output', exist_ok=True)

    for folder_index in range(1, num_folders + 1):
        output_directory = f"output/output {folder_index}"

        # Create a directory for the modified videos
        os.makedirs(output_directory, exist_ok=True)

        input_directory = "./input"

        # Process and modify videos
        video_files = [f for f in os.listdir(input_directory) if f.lower().endswith(
            ('.mp4'))]

        for video_file in video_files:
            input_video_file = os.path.join(input_directory, video_file)
            process_video(input_video_file)
            total_cleaned += 1  # Increment the total cleaned count

    print(f"{total_cleaned} videos cleaned")
