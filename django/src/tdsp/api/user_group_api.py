from django.contrib.auth.models import User

from rest_framework import viewsets

from ..serializers.user_serializers import UserSerializer, UserCreateSerializer
from ..permissions.permissions import IsAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing user accounts. Only admins are allowed to view or edit user accounts.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        """
        Return the appropriate serializer class depending on the action being performed.

        :return Serializer class: The serializer class to use.
        """
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
