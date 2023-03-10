import base64
import imghdr
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import Image, generate_image_filename


class ImageSerializer(serializers.ModelSerializer):
    file = serializers.CharField(write_only=True)

    class Meta:
        model = Image
        fields = ('id', 'file', 'url')
        read_only_fields = ('id', 'url')

    def create(self, validated_data):
        file_data = validated_data.pop('file')
        # Decode the base64-encoded image data
        decoded_img = base64.b64decode(file_data)

        # Extract the file extension from the decoded data
        ext = imghdr.what(None, h=decoded_img)
        if not ext:
            raise serializers.ValidationError('Unable to determine file type')

        # Generate a random filename with the correct extension
        generated_filename = generate_image_filename(None, f'image.{ext}')

        # create a ContentFile object from the decoded data
        img_file = ContentFile(decoded_img, name=generated_filename)

        # set the file attribute to the ContentFile object
        validated_data['file'] = img_file

        # call the parent create method to create the Image object
        return super().create(validated_data)
