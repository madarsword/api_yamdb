from rest_framework import serializers
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(
        slug_field='username',
        read_only=True,
    )
    title = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date',
        )

    def validate(self, data):
        """Не дает юзерам оставлять больше одного отзыва."""
        request = self.context.get('request')
        if not request.method == 'POST':
            return data
        author = request.user
        # title_id = request.kwargs.get('title_id')
            # не понимаю пока, как это писать. Написано точно неправильно,
            # в request'е нет 'title_id'
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Нельзя оставлять больше одного отзыва на произведение'
            )
        return data

from datetime import datetime

from reviews.models import Genre, Category, Title


class GenreSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего')
        return value

    def to_representation(self, instance):
        self.fields['category'] = CategorySerializer()
        return super().to_representation(instance)
