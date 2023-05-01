from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    CommentViewSet,
    ReviewViewSet,
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet
)


router_v1 = DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments/(?P<comment_id>\d+)', CommentViewSet, basename='comments')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(
    r'categories/(?P<slug>[\w-]+)',
    CategoryViewSet,
    basename='category'
)
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'genres/(?P<slug>[\w-]+)', GenreViewSet, basename='genre')
#router_v1.register(r'users', basename='users')



urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # path('v1/auth/token/',),
    # path('v1/auth/signup/',),
]
