import base64
import unittest
from PIL import Image as Pil
from io import BytesIO
from django.core.files.base import ContentFile

from ...tools.image_server_tools import (generate_image_name, decode_image_file,
                                         send_image_to_flask_server, send_image, generate_image)


class TestImageServerTools(unittest.TestCase):

    def test_generate_image_name(self):
        decoded_img = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeA"
                                       "AAADElEQVQImWNgYGBgAAAABQABXvMqOgAAAABJRU5ErkJggg==")
        image_name, ext = generate_image_name(decoded_img)
        self.assertEqual(len(image_name), 36)
        self.assertEqual(ext, 'png')

    def test_decode_image_file(self):
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
        pass

    def test_generate_image(self):
        img_width = 100
        img_height = 100
        encoded_image = generate_image(img_width, img_height)
        decoded_img = base64.b64decode(encoded_image)
        img_bytes = BytesIO(decoded_img)
        img = Pil.open(img_bytes)
        self.assertEqual(img.size, (img_width, img_height))
