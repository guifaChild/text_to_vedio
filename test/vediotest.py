# -*- coding:utf-8 -*-
"""
作者：张贵发
日期：2023年08月06日
描述：
"""

image_path = '../data/data_image/ce11/ce11/0.png'

from moviepy.editor import *


def zoom_in(image, duration, target_size):
    # Resize the image to the target size
    resized_image = image.resize(target_size)

    # Define a lambda function to animate the size of the image
    def resize_func(t):
        current_size = tuple(int(s + (e - s) * t) for s, e in zip(image.size, target_size))
        current_image = image.resize(current_size)
        return current_image.img  # Return the actual image data (numpy array)

    # Create a video clip from the resized image
    zoom_clip = VideoClip(resize_func, duration=duration)

    return zoom_clip


# Load your image
# image_path = 'path/to/your/image.jpg'
image = ImageClip(image_path)

# Define the target size you want to zoom into
target_size = (2 * image.w, 2 * image.h)

# Define the duration of the zoom animation (in seconds)
zoom_duration = 5

# Create the zoom-in video clip
zoom_in_clip = zoom_in(image, zoom_duration, target_size)

# Set the FPS attribute for the video clip
zoom_in_clip = zoom_in_clip.set_fps(1)  # Change 24 to your desired frame rate

# Export the video file
output_path = 'video.mp4'
zoom_in_clip.write_videofile(output_path, codec='libx264')
