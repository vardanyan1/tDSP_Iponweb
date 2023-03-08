import json

from rest_framework import viewsets, status
from rest_framework.response import Response
from ..dsp.models.creative_model import CreativeModel
from ..dsp.models.categories_model import CategoryModel, SubcategoryModel
from ..serializers.serializers import CreativeSerializer
import requests


class CreativeViewSet(viewsets.ModelViewSet):
    queryset = CreativeModel.objects.all()
    serializer_class = CreativeSerializer

    def create(self, request, *args, **kwargs):
        # Get data from request
        external_id = request.data.get('external_id')
        name = request.data.get('name')
        campaign_str = request.data.get('campaign')
        categories_str = request.data.get('categories')
        categories = json.loads(categories_str)

        campaign_dict = json.loads(campaign_str)
        campaign_id = campaign_dict['id']
        # campaign_id = request.data.get('campaign')['id']  # Need do consult for campaign object in multipart/form-data
        # campaign_id = request.data.get('campaign')
        image_file = request.FILES.get('file')
        print(image_file)

        # Save image to separate service and get url
        image_url = save_image(image_file)

        # Create creative
        creative = CreativeModel.objects.create(
            external_id=external_id,
            name=name,
            campaign_id=campaign_id,
            image_url=image_url
        )

        # Add categories to creative
        for category in categories:
            code = category['code']
            code = "".join([i for i in code if i != "_"])
            if '-' in code:
                sub_category_obj = SubcategoryModel.objects.get(IAB_Code=code)
                creative.categories.add(sub_category_obj)
            else:
                category = CategoryModel.objects.get(IAB_Code=code)
                sub_categories = SubcategoryModel.objects.filter(category=category)
                for sub_category in sub_categories:
                    creative.categories.add(sub_category)

        # Serialize and return created creative data
        serializer = self.get_serializer(creative)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def save_image(image_file):
    # Use requests library to post the image to a separate service
    # and get the url for the saved image
    # To get ip of server run: docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' 2e2c390ab42a

    url = 'http://172.26.0.5:8001/save_image/'

    response = requests.post(url, files={'file': image_file})
    image_url = response.json().get('url')
    return image_url
