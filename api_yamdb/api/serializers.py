from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Review, Comment

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
