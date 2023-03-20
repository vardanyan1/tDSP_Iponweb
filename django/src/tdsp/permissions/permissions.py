from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow read access to any user, but only write access to admins.

    Usage:
        Use this permission class with Django REST Framework views that provide read-only access to a resource for
         all users, but restrict write access to administrators. To use this permission class, add it to
          the `permission_classes` attribute of a Django REST framework view that inherits from `views.APIView`
          or one of its subclasses.

    Methods:
        has_permission(self, request, view) -- Check whether the requesting user has permission to access the view.
                                                Returns `True` if the requesting user is authenticated,
                                                `False` otherwise.
        has_object_permission(self, request, view, obj) -- Check whether the requesting user has permission to access
                                                            a specific object. Returns `True` if the requesting user is
                                                             authenticated and is a staff member, `False` otherwise.

    Examples:
        from rest_framework import views
        from rest_framework.permissions import IsAuthenticated

        class MyReadOnlyView(views.APIView):
            permission_classes = [IsAuthenticatedOrReadOnly]
            ...
    """
    def has_permission(self, request, view):
        # Authenticated users only can see list view
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request so we'll always
        # allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the admins
        return request.user.is_staff
