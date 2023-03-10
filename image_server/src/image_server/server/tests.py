import base64
from PIL import Image as pil
from io import BytesIO

from django.core.files.base import ContentFile
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from .models import Image, generate_image_filename


class ImageTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.image_data = {'file': SimpleUploadedFile('test_image.png', b'')}

    @staticmethod
    def create_test_image():
        # Create a 100x100 pixel RGB image with a red background
        img = pil.new('RGB', (100, 100), color='red')

        # Encode the image as PNG and get the bytes
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()

        # Encode the image bytes as base64
        encoded_image = base64.b64encode(img_bytes)

        return encoded_image

    def test_generate_image_filename(self):
        instance = None
        filename = 'test_image.png'
        result = generate_image_filename(instance, filename)
        self.assertRegex(result, r'^[A-Za-z0-9_]{32}\.png$')

    def test_image_creation(self):
        # Create a test image
        image_data = self.create_test_image()  # base64 encoded image data
        image_file = ContentFile(base64.b64decode(image_data), name='test.png')

        # Create an Image object
        image = Image.objects.create(file=image_file)

        # Check that the file was saved correctly
        self.assertEqual(image.file.read(), base64.b64decode(image_data))
        self.assertEqual(image.url, f'http://localhost:8001/media/{image.file.name}')

    def test_save_image_view(self):

        image_data = self.create_test_image()  # base64 encoded image data

        response = self.client.post('/save_image/', {'file': image_data}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertRegex(response.data['url'], r'^http://localhost:8001/media/[A-Za-z0-9_]{32}\.png$')

    def test_save_image_view_invalid_data(self):
        response = self.client.post('/save_image/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
