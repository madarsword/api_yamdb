from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CommentViewSet, ReviewViewSet, TitleViewSet

router_v1 = DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)', ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments/(?P<comment_id>\d+)', CommentViewSet, basename='comments')
router_v1.register(r'categories', basename='categories')
router_v1.register(r'genres', basename='genres')
router_v1.register(r'users', basename='users')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
