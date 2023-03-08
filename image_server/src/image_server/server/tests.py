from PIL import Image as pil
from io import BytesIO

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status

from .models import Image, generate_image_filename


class ImageTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.image_data = {'file': SimpleUploadedFile('test_image.png', b'')}

    def test_generate_image_filename(self):
        instance = None
        filename = 'test_image.png'
        result = generate_image_filename(instance, filename)
        self.assertRegex(result, r'^[A-Za-z0-9_]{32}\.png$')

    def test_image_save(self):
        image = Image.objects.create(file=SimpleUploadedFile('test_image.png', b''))
        self.assertEqual(image.url, f'http://localhost:8001/media/{image.file.name}')

    @staticmethod
    def create_test_image():
        # Create a 100x100 pixel RGB image with a red background
        img = pil.new('RGB', (100, 100), color='red')
        # Save the image to a byte stream
        stream = BytesIO()
        img.save(stream, format='PNG')
        # Return the byte stream content as bytes
        return stream.getvalue()

    def test_save_image_view(self):
        file_data = {'file': SimpleUploadedFile('test_image.png', self.create_test_image())}
        response = self.client.post('/save_image/', file_data, format='multipart')
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertRegex(response.data['url'], r'^http://localhost:8001/media/[A-Za-z0-9_]{32}\.png$')

    def test_save_image_view_invalid_data(self):
        response = self.client.post('/save_image/', {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
