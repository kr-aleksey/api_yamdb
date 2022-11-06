import statistics
from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
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


class TitleGetSerializer(serializers.ModelSerializer):

    # rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            # 'rating',
            'genre', 'category',
        )

    def get_rating(self, obj):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review_list = title.reviews.select_related('title')
        score_review_list = []
        for review in review_list:
            score_review_list += review.score
        rating = statistics.mean(score_review_list)
        return rating


class TitlePostSerializer(serializers.ModelSerializer):

    description = serializers.StringRelatedField(required=False,)
    genre = GenreSerializer(many=True,)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category',
        )

    def validate_year(self, value):
        year_today = date.today().year
        if not (0 < value <= year_today):
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего'
            )
        return value

    def create(self, validated_data):
        genres_slugs = validated_data.pop('genre')
        category_slug = validated_data.pop('category')

        title = Title.objects.create(**validated_data)

        for slug in genres_slugs:
            this_genre = Genre.objects.get(slug=slug)
            title.genre.add(this_genre)

        this_category = Category.objects.get(slug=category_slug)
        title.category.add(this_category)

        return title
