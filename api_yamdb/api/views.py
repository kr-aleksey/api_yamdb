from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.validators import ValidationError
from rest_framework import views, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Review, Title
from . import serializers
from .permissions import AuthorOrReadOnly
from users.services import send_confirmation_mail

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'


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
