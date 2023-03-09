from rest_framework import viewsets, permissions
from rest_framework.response import Response

from ..dsp.models.game_config_model import ConfigModel
from ..permissions.permissions import IsAdminOrReadOnly
from ..serializers.serializers import ConfigSerializer, ConfigCreateSerializer


class ConfigViewSet(viewsets.ModelViewSet):
    queryset = ConfigModel.objects.all()
    serializer_class = ConfigSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return ConfigCreateSerializer
        return ConfigSerializer

    def create(self, request, *args, **kwargs):
        # Remove the 'current' field from the request data
        data = request.data.copy()
        data.pop('current', None)

        # Set the 'current' field to True
        data['current'] = True

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
