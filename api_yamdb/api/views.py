import random
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from reviews.models import Category, Genre, Review, Title
from users.models import User
from api.filters import TitleFilter
from .extensions import send_confirmation_code
from .permissions import (IsAuthorOrReadOnly, IsAdmin,
                          IsModerator, ReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializer, TitleCreateSerializer,
                          UserSerializer, SignUpSerializer,
                          TokenSerializer)


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin | ReadOnly]
    search_fields = ['name']


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdmin | ReadOnly]
    search_fields = ['name']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = [IsAdmin | ReadOnly]

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAdmin | IsModerator | IsAuthorOrReadOnly,
    ]

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAdmin | IsModerator | IsAuthorOrReadOnly,
    ]

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get('username')
        if username == 'me':
            return Response('Нельзя использовать имя <me>.',
                            status=status.HTTP_400_BAD_REQUEST)
        email = serializer.data.get('email')
        confirmation_code = random.randint(100000, 999999)
        send_confirmation_code(username, email, confirmation_code)
        if User.objects.filter(username=username).exists():
            if User.objects.filter(username=username, email=email).exists():
                found_user = User.objects.get(username=username)
                found_user.confirmation_code = confirmation_code
                found_user.save()
                return Response(serializer.validated_data,
                                status=status.HTTP_200_OK
                                )
            return Response('Email пользователя указан неправильно.',
                            status=status.HTTP_400_BAD_REQUEST
                            )
        if User.objects.filter(email=email).exists():
            found_user = User.objects.get(email=email)
            found_user.confirmation_code = confirmation_code
            found_user.save()
            return Response(serializer.validated_data,
                            status=status.HTTP_400_BAD_REQUEST
                            )
        User.objects.create_user(username=username,
                                 email=email,
                                 confirmation_code=confirmation_code
                                 )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        if User.objects.filter(username=username).exists():
            current_user = User.objects.get(username=username)
            if current_user.confirmation_code != confirmation_code:
                return Response('Неправильный код подтверждения.',
                                status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken.for_user(current_user).access_token
            current_user.confirmation_code = None
            return Response(token, status=status.HTTP_200_OK)
        else:
            return Response('Пользователя не существует.',
                            status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
