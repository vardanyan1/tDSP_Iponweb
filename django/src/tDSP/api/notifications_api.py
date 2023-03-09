from rest_framework import viewsets
from rest_framework.response import Response
from ..dsp.models.notification_model import Notification
from ..serializers.serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
