from rest_framework import serializers
from reviews.models import Review, Comment


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
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Нельзя оставлять больше одного отзыва на произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id', 'text', 'author', 'pub_date'
        )
