from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    CommentViewSet, ReviewViewSet, 
    TitleViewSet, CategoryViewSet,
    GenreViewSet, UserViewSet,
    SignUpView
)


router_v1 = DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)',
    ReviewViewSet,
    basename='reviews'
    )
router_v1.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)'
    r'/comments/(?P<comment_id>\d+)',
    CommentViewSet,
    basename='comments'
    )


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # path('v1/auth/token/', .as_view(), name=''),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
]
