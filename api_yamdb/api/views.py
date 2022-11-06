from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, views, viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.services import send_confirmation_mail

from . import serializers
from .filters import TitleFilter, UserFilter
# from .filters CategoryFilter, GenreFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import AdminOrReadOnly, AuthorOrReadOnly, UserAPIPermissions

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [UserAPIPermissions]
    lookup_field = 'username'

    filterset_class = UserFilter
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('username',)

    def get_object(self):
        username = self.kwargs.get('username')
        if username == 'me':
            user = self.request.user
        else:
            user = get_object_or_404(User, username=username)
        self.check_object_permissions(self.request, user)
        return user

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        user = self.request.user
        if (user == serializer.instance
                and not user.is_admin()
                and 'role' in serializer.validated_data):
            serializer.validated_data.pop('role')
        serializer.save()


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


class CommonViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrReadOnly, )


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'

    # filterset_class = CategoryFilter
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'

    # filterset_class = GenreFilter
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnly,)

    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'POST' or 'PATCH':
            return serializers.TitlePostSerializer
        return serializers.TitleGetSerializer


class ReviewViewSet(CommonViewSet):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

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
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        title = get_object_or_404(Title, id=self.kwargs['title_id'])

        if review.title != title:
            raise ValidationError('Ревью не соответствует Произвдению')

        serializer.save(
            author=self.request.user,
            review=review
        )
