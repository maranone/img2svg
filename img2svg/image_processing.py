import requests
from PIL import Image
from io import BytesIO
import os
from urllib.parse import urlparse

def download_and_resize_image(image_source, resize_original=2, min_width=80):
    # Determine if the image source is a URL or a local file path
    if image_source.startswith('http://') or image_source.startswith('https://'):
        response = requests.get(image_source)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            # Extract filename from URL without query params
            parsed_url = urlparse(image_source)
            original_filename = os.path.basename(parsed_url.path)
        else:
            raise ValueError('Failed to download the image.')
    elif os.path.isfile(image_source):
        image = Image.open(image_source)
        # Extract the base filename from the local path
        original_filename = os.path.basename(image_source)
    else:
        raise ValueError('Invalid URL or file path.')

    # Resize the image
    new_width = image.width // resize_original
    new_height = image.height // resize_original
    if new_width < min_width:
        new_width = min_width
        new_height = int(image.height * (new_width / image.width))

    # Save the resized image with a name derived from the original filename
    base_name, ext = os.path.splitext(original_filename)
    resized_filename = f"{base_name}_resized.png"
    resized_image = image.resize((new_width, new_height))
    resized_image.save(resized_filename, 'PNG')

    return resized_filename, new_width, new_height
