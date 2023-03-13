from rest_framework import viewsets, permissions
from rest_framework.response import Response

from ..dsp.models.campaign_model import CampaignModel
from ..dsp.models.categories_model import SubcategoryModel
from ..dsp.models.creative_model import CreativeModel
from ..dsp.models.game_config_model import ConfigModel
from ..serializers.serializers import ConfigSerializer, ConfigCreateSerializer, CampaignSerializer, CreativeSerializer

from ..tools.image_server_tools import generate_image, save_image_to_minio


class ConfigViewSet(viewsets.ModelViewSet):
    queryset = ConfigModel.objects.all()
    serializer_class = ConfigSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return ConfigCreateSerializer
        return ConfigSerializer

    def create(self, request, *args, **kwargs):
        # Delete the old config object, if it exists
        ConfigModel.objects.filter(current=True).delete()

        # Remove the 'current' field from the request data
        data = request.data.copy()
        data.pop('current', None)

        # Set the 'current' field to True
        data['current'] = True

        # Set the rounds_left to number of impressions total
        data['rounds_left'] = data['impressions_total']

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        config = serializer.save()

        if data['mode'] == "free":
            campaign = CampaignModel.objects.create(name='Free Campaign', config=config, budget=data['budget'])
            CampaignSerializer(campaign)

            # Create creative
            image_url = save_image_to_minio(generate_image(300, 200))
            creative = CreativeModel.objects.create(external_id="free_creative_id", name="Free Creative",
                                                    campaign_id=campaign.id, url=image_url)
            subcategory = SubcategoryModel.objects.get(code="IAB6-6")
            creative.subcategories.add(subcategory)
            CreativeSerializer(creative)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=200, headers=headers)
