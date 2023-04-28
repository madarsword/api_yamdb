from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Title
from .serializers import TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('name', 'year', 'description', 'genre', 'category')
