from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.validators import ValidationError

from reviews.models import Category, Genre, Title, Review
from . import serializers
from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import (
    IsAdminOrReadOnly,
    IsModeratorOrReadOnly,
    IsAuthorOrReadOnly
)


class CommonViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthorOrReadOnly | IsModeratorOrReadOnly | IsAdminOrReadOnly,
    )


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title
        .objects
        .annotate(Avg('reviews__score'))
        .select_related('category')
        .prefetch_related('genre')
        .order_by('name')
    )
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = serializers.TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class ReviewViewSet(CommonViewSet):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
    # Яков:
     # Дублируем код получения ревью, его нужно вынести в отдельный метод.
        return Review.objects.filter(
            title__id=self.kwargs['title_id']
        ).select_related(
            'author'
        )

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
        return review.comments.all().select_related(
            'author'
        )

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        title = get_object_or_404(Title, id=self.kwargs['title_id'])

        if review.title != title:
            raise ValidationError('Ревью не соответствует Произведению')

        serializer.save(
            author=self.request.user,
            review=review
        )
