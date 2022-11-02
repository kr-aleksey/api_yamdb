from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Review
from .permissions import AuthorOrReadOnly
from . import serializers

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
        serializer.save(
            author=self.request.user,
            # title=Title.objects.get(id=self.kwargs['title_id'])
        )


class CommentViewSet(CommonViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=Review.objects.get(id=self.kwargs['review_id'])
        )



