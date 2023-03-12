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
        campaign_id = request.data.get('campaign')['id']
        encoded_image = request.data.get('file')
        categories = request.data.get('categories')

        # Save image to separate service and get url
        image_url = save_image_to_minio(encoded_image)

        # Create creative
        creative = CreativeModel.objects.create(external_id=external_id, name=name,
                                                campaign_id=campaign_id, url=image_url)

# TODO: optimize to use a single db query
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

