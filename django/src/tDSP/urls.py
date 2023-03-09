"""tDSP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from .api.bid_request_api import BidViewSet
from .api.user_group_api import UserViewSet
from .api.game_config_api import ConfigViewSet
from .api.categories_api import CategoryViewSet, SubcategoryViewSet
from .api.creative_api import CreativeViewSet
from .api.campaign_api import CampaignViewSet


router = routers.DefaultRouter()

# Main functionality
router.register(r'game/configure', ConfigViewSet)
router.register(r'api/creatives', CreativeViewSet)
router.register(r'api/campaigns', CampaignViewSet)
router.register(r'rtb/bid', BidViewSet, basename='rtb-bid')


# Additional
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path("", include("rest_framework.urls")),
]
