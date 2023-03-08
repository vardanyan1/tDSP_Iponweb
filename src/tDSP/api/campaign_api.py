from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from ..serializers.serializers import CampaignSerializer
from ..dsp.models.campaign_model import CampaignModel
from ..dsp.models.game_config_model import ConfigModel


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = CampaignModel.objects.all()
    serializer_class = CampaignSerializer

