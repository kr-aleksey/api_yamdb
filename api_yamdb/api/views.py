from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.validators import ValidationError

from reviews.models import Review, Title
from . import serializers
from .permissions import AuthorOrReadOnly

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


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
