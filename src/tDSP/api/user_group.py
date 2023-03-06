from django.contrib.auth.models import User

from rest_framework import viewsets

from ..serializers.serializers import UserSerializer, UserCreateSerializer
from ..permissions.permissions import IsAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to be viewed or edited only by admin.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
