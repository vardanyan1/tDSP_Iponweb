from django.db import models
from django.utils.crypto import get_random_string


def generate_image_filename(instance, filename):
    ext = filename.split('.')[-1]
    return f'{get_random_string(length=32)}.{ext}'


class Image(models.Model):
    file = models.ImageField(upload_to=generate_image_filename)
    url = models.URLField()

    def save(self, *args, **kwargs):
        # Save the image file to disk
        super().save(*args, **kwargs)

        # Set the URL for the saved image
        self.url = f'http://localhost:8001/media/{self.file.name}'
        super().save(update_fields=['url'])
