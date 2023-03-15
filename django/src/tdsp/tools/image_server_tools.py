import base64
import imghdr
from io import BytesIO
from PIL import Image as Pil
import requests
import uuid
import environ

from django.core.files.base import ContentFile

env = environ.Env()


# TODO: revisit return types

def generate_image_name(decoded_img):
    ext = imghdr.what(None, h=decoded_img)

    # Generate a random 32-character name
    name = str(uuid.uuid4().hex)[:32]

    # Combine the name and extension to create the final image name
    image_name = f"{name}.{ext}"

    return image_name, ext


def get_content_type_from_ext(ext):
    content_type = 'application/octet-stream'

    if ext:
        if ext == 'jpeg':
            content_type = 'image/jpeg'
        elif ext == 'png':
            content_type = 'image/png'

    return content_type


# TODO: example unit test
# describe('get_content_type_from_ext', () => {
#     it('should return default content type if invalid extension was provided', () => {
# result = get_content_type_from_ext('asdasd')
# assert(res)
# })
# })
def send_image_to_flask_server(base64_image):
    image_file = decode_image_file(base64_image)

    url = "http://image_server_flask:8080/upload"

    files = {'file': image_file}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        return response.json()['url']
    else:
        print(f"Error sending image to Flask server: {response.text}")
        return None


def decode_image_file(base64_image):
    # Decode the base64-encoded image
    decoded_img = base64.b64decode(base64_image)

    # create a ContentFile object from the decoded data
    name, ext = generate_image_name(decoded_img)
    content_type = get_content_type_from_ext(ext)
    img_file = ContentFile(decoded_img, name=name)

    return img_file


def send_image(base64_image):
    url = send_image_to_flask_server(base64_image)
    return url


def generate_image(img_width, img_height):
    # Create a 100x100 pixel RGB image with a red background
    img = Pil.new('RGB', (img_width, img_height), color='red')

    # Encode the image as PNG and get the bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()

    # Encode the image bytes as base64
    encoded_image = base64.b64encode(img_bytes).decode('utf-8')

    return encoded_image
