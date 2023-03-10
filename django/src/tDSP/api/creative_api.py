import json
import requests
import os
import logging
import boto3
from botocore.exceptions import ClientError

from rest_framework import viewsets, status
from rest_framework.response import Response
from ..dsp.models.creative_model import CreativeModel
from ..dsp.models.categories_model import CategoryModel, SubcategoryModel
from ..serializers.serializers import CreativeSerializer
from ..tools.image_server_tools import save_image_to_minio


class CreativeViewSet(viewsets.ModelViewSet):
    queryset = CreativeModel.objects.all()
    serializer_class = CreativeSerializer

    def create(self, request, *args, **kwargs):
        # Get data from request
        external_id = request.data.get('external_id')
        name = request.data.get('name')
        campaign_id = json.loads(request.data.get('campaign'))['id']
        encoded_image = request.data.get('file')
        categories = json.loads(request.data.get('categories'))

        # Save image to separate service and get url
        # image_url = save_image(encoded_image)
        image_url = save_image_to_minio(encoded_image)

        # Create creative
        creative = CreativeModel.objects.create(external_id=external_id, name=name,
                                                campaign_id=campaign_id, url=image_url)

        # Add categories to creative
        for category in categories:
            code = category['code']
            code = "".join([i for i in code if i != "_"])
            if '-' in code:
                sub_category_obj = SubcategoryModel.objects.get(code=code)
                creative.categories.add(sub_category_obj)
            else:
                category = CategoryModel.objects.get(code=code)
                sub_categories = SubcategoryModel.objects.filter(category=category)
                for sub_category in sub_categories:
                    creative.categories.add(sub_category)

        # Serialize and return created creative data
        serializer = self.get_serializer(creative)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def save_image(encoded_image):
    # TODO understand how can on server contact another without IP

    # Use requests library to post the image to a separate service
    # and get the url for the saved image
    # To get ip of server run: docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' 2e2c390ab42a

    url = 'http://172.26.0.4:8001/save_image/'
    response = requests.post(url, json={'file': encoded_image})
    image_url = response.json().get('url')
    return image_url

    # TODO Implement File Server
    # """Upload a file to an S3 bucket
    #
    #     :param file_name: File to upload
    #     :param bucket: Bucket to upload to
    #     :param object_name: S3 object name. If not specified then file_name is used
    #     :return: True if file was uploaded, else False
    #     """
    # bucket = 'tsdp-image-server'
    # # If S3 object_name was not specified, use file_name
    # if image_file.name is None:
    #     object_name = os.path.basename(image_file.name)
    #
    # # Upload the file
    # s3_client = boto3.client('s3')
    # try:
    #     response = s3_client.upload_file(image_file.name, bucket)
    # except ClientError as e:
    #     logging.error(e)
    #     return False
    # return True
