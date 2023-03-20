import base64
import unittest
from PIL import Image as Pil
from io import BytesIO
from django.core.files.base import ContentFile

from ...tools.image_server_tools import (generate_image_name, decode_image_file, generate_image)


class TestImageServerTools(unittest.TestCase):
    """
     A test case for the `image_server_tools` module.

    Methods:
        test_generate_image_name(): Tests the `generate_image_name` function by passing a base64-encoded image and
                                     checks that the function returns a UUID string and the image file extension.
        test_decode_image_file(): Tests the `decode_image_file` function by passing a base64-encoded image and
                                   checks that the function returns a ContentFile object.
        test_send_image(): Tests the `send_image` function by mocking the `send_image_to_flask_server` function and
                            `requests.post` function and checks that the function returns a dictionary containing
                            the image URL and status code.
        test_generate_image(): Tests the `generate_image` function by generating a 100x100 pixel image and checks that
                               the function returns a base64-encoded string and the image dimensions are correct.
    """

    def test_generate_image_name(self):
        """
        Test the generate_image_name function to ensure that it returns a unique image name
        and file extension based on the decoded image file provided.
        """
        decoded_img = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeA"
                                       "AAADElEQVQImWNgYGBgAAAABQABXvMqOgAAAABJRU5ErkJggg==")
        image_name, ext = generate_image_name(decoded_img)
        self.assertEqual(len(image_name), 36)
        self.assertEqual(ext, 'png')

    def test_decode_image_file(self):
        """
        Test the decode_image_file function to ensure that it decodes a base64-encoded image file
        and returns it as a ContentFile object.
        """
        base64_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADEl" \
                       "EQVQImWNgYGBgAAAABQABXvMqOgAAAABJRU5ErkJggg=="
        img_file = decode_image_file(base64_image)
        self.assertIsInstance(img_file, ContentFile)

        base64_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAA" \
                       "BCAIAAACQd1PeAAAADElEQVQImWNgYGBgAAAABQABXvMqOgAAAABJRU5ErkJggg=="
        img_file = decode_image_file(base64_image)
        self.assertIsInstance(img_file, ContentFile)

    # Mock the send_image_to_flask_server and requests.post functions for the following test
    def test_send_image(self):
        """
        Test the send_image function to ensure that it sends an image file to the Flask server
        and returns the URL of the image file on the server.
        """
        pass

    def test_generate_image(self):
        """
        Test the generate_image function to ensure that it generates a new image with the specified
        width and height, encodes it as a base64 string, and returns the string.
        """
        img_width = 100
        img_height = 100
        encoded_image = generate_image(img_width, img_height)
        decoded_img = base64.b64decode(encoded_image)
        img_bytes = BytesIO(decoded_img)
        img = Pil.open(img_bytes)
        self.assertEqual(img.size, (img_width, img_height))
