from rest_framework import viewsets

from ..dsp.models.campaign_model import CampaignModel

from ..serializers.campaign_serializer import CampaignSerializer


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = CampaignModel.objects.all()
    serializer_class = CampaignSerializer

