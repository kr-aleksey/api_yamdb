from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Slug категории',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:50]


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Slug жанра',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:50]


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
    )
    description = models.TextField(
        blank=True, null=True,
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Slug жанра',
        # on_delete=models.SET_NULL, - такого параметра нет у ManyToManyField
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        blank=True,     # это обязательно при
        null=True,      # on_delete=models.SET_NULL
        verbose_name='Slug категории',
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:50]
