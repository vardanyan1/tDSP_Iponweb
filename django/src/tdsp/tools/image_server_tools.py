import base64
import os
import imghdr
from io import BytesIO
from PIL import Image as Pil
import requests
import uuid

from django.core.files.base import ContentFile


def send_image(base64_image: str) -> str:
    """
    Send a base64-encoded image to the Flask server and return the URL of the stored image.

    :param base64_image: A base64-encoded image string
    :return: The URL of the stored image if successful, None otherwise
    """
    try:
        url = send_image_to_flask_server(base64_image)
        return url
    except ImageUploadError as e:
        # Handle the error (e.g., log the error message, return an error message, etc.)
        print(e)
        return "Error uploading the image"


def send_image_to_flask_server(base64_image: str) -> str:
    """
    Send a base64-encoded image to the Flask server for storage.

    :param base64_image: A base64-encoded image string
    :return: The URL of the stored image if successful
    :raises ImageUploadError: If an error occurs while sending the image to the Flask server
    """
    image_file = decode_image_file(base64_image)

    url = f"http://{os.environ.get('IMAGE_SERVER')}/upload"

    files = {'file': image_file}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        return response.json()['url']
    else:
        raise ImageUploadError(f"Error sending image to Flask server: {response.text}")


def decode_image_file(base64_image: str) -> ContentFile:
    """
    Decode a base64-encoded image and create a ContentFile object from the decoded data.

    :param base64_image: A base64-encoded image string
    :return: A ContentFile object containing the decoded image data
    """
    # Remove the data URL part, if present
    if base64_image.startswith('data:'):
        base64_image = base64_image.split('base64,')[-1]

    # Add padding if necessary
    padding = 4 - len(base64_image) % 4
    if padding:
        base64_image += "=" * padding

    # Decode the base64-encoded image
    decoded_img = base64.b64decode(base64_image)

    # create a ContentFile object from the decoded data
    name, ext = generate_image_name(decoded_img)
    img_file = ContentFile(decoded_img, name=name)

    return img_file


def generate_image_name(decoded_img: bytes) -> tuple[str, str]:
    """
    Generate a unique image name with the appropriate extension for the given decoded image.

    :param decoded_img: Decoded image bytes
    :return: A tuple containing the generated unique image name and the extension
    """
    ext = imghdr.what(None, h=decoded_img)

    # Generate a random 32-character name
    name = str(uuid.uuid4().hex)[:32]

    # Combine the name and extension to create the final image name
    image_name = f"{name}.{ext}"

    return image_name, ext


def generate_image(img_width: int, img_height: int) -> str:
    """
    Generate a red RGB image with the given dimensions and return it as a base64-encoded string.

    :param img_width: The width of the generated image in pixels
    :param img_height: The height of the generated image in pixels
    :return: A base64-encoded string representing the generated image
    """
    # Create a 100x100 pixel RGB image with a red background
    img = Pil.new('RGB', (img_width, img_height), color='red')

    # Encode the image as PNG and get the bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()

    # Encode the image bytes as base64
    encoded_image = base64.b64encode(img_bytes).decode('utf-8')

    return encoded_image


class ImageUploadError(Exception):
    pass
