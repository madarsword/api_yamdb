from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import TitleViewSet

router_v1 = SimpleRouter()
router_v1.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router_v1.urls)),
]
