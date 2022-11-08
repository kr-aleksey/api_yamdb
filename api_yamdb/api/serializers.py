from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
# Яков:
# Я бы разнес сериализаторы и вьюхи по разным приложениям, чтобы у нас не было смешения логики.
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                f'Использовать имя "{username}" запрещено!')
        return username


class MeUserSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)

    class Mate:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class SignupSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )


class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(
        max_length=settings.CONFIRMATION_CODE_LEN
    )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField()
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'rating', 'genre', 'category',
        )
        read_only_fields = ('id', 'rating')

    def get_rating(self, obj):
        score_review_list = Review.objects.filter(
            title=obj.id).aggregate(Avg('score'))
        rating = score_review_list['score__avg']
        if rating is None:
            return None
        return float('{:.1f}'.format(rating))

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = CategorySerializer(instance.category).data
        response['genre'] = GenreSerializer(instance.genre, many=True).data
        return response

    def validate_year(self, value):
        year_now = datetime.now().year
        if not (0 < value <= year_now):
            raise serializers.ValidationError(
                'Проверьте год создания произведения!')
        return value
