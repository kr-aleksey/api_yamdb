from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from rest_framework.filters import SearchFilter

from reviews.models import Category, Genre
from reviews.models import Title


User = get_user_model()


class UserFilter(SearchFilter):

    class Meta:
        model = User
        fields = ('username',)


class TitleFilter(DjangoFilterBackend):

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')


class CategoryFilter(SearchFilter):

    class Meta:
        model = Category
        fields = ('name',)


class GenreFilter(SearchFilter):

    class Meta:
        model = Genre
        fields = ('name',)
