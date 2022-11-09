from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, views, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Title, Review
from users.services import send_confirmation_mail
from . import serializers
from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import (
    AdminOrReadOnly,
    UserAPIPermissions,
    IsAdminOrReadOnly,
    IsModeratorOrReadOnly,
    IsAuthorOrReadOnly
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [UserAPIPermissions]
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SignupView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serializers.SignupSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            email = serializer.data['email']
            confirmation_code = User.objects.make_random_password(
                length=settings.CONFIRMATION_CODE_LEN
            )
            user = User.objects.create_user(
                username=username,
                email=email,
                password=confirmation_code
            )
            send_confirmation_mail(user, confirmation_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serializers.TokenObtainSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        username = serializer.data['username']
        confirmation_code = serializer.data['confirmation_code']
        get_object_or_404(User, username=username)
        user = authenticate(username=username, password=confirmation_code)
        if user is None:
            return Response(
                {"detail": "Ошибка аутентификации"},
                status=status.HTTP_400_BAD_REQUEST
            )
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK
        )


class MeUserView(views.APIView):
    # Яков:
    # Я бы эту вьюху писал либо с помощью @action,
    # либо сделал дженерик класс в котором были бы только put/get методы.

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = serializers.MeUserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = serializers.MeUserSerializer(data=request.data,
                                                  instance=user,
                                                  partial=True)
        if serializer.is_valid():
            # Яков:
            # Я бы ставли флаг raise_exception=True, чтобы не
            # создавать лишней вложенности.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommonViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthorOrReadOnly | IsModeratorOrReadOnly | IsAdminOrReadOnly,
    )


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.select_related('category', 'genre')
    permission_classes = (AdminOrReadOnly,)
    serializer_class = serializers.TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class ReviewViewSet(CommonViewSet):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(title__id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        author = self.request.user
        if Review.objects.filter(
            title=title,
            author=author
        ).exists():
            raise ValidationError('Нельзя размещать более одного ревью.')

        serializer.save(
            title=title,
            author=author,
        )


class CommentViewSet(CommonViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return self.get_review().comments.all()

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def perform_create(self, serializer):
        review = self.get_review()
        title = get_object_or_404(Title, id=self.kwargs['title_id'])

        if review.title != title:
            raise ValidationError('Ревью не соответствует Произведению')

        serializer.save(
            author=self.request.user,
            review=review
        )
