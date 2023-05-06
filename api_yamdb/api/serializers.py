from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.validators import validate_username


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date',
        )

    def validate(self, data):
        request = self.context.get('request')
        if not request.method == 'POST':
            return data
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=request.user, title=title_id).exists():
            raise serializers.ValidationError(
                'Нельзя оставлять больше одного отзыва на произведение'
            )
        return data


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = (
            'id', 'text', 'author', 'pub_date'
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(validate_username,)
    )
    email = serializers.EmailField(max_length=254, required=True)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(validate_username,)
    )
    confirmation_code = serializers.CharField(max_length=6, required=True)
