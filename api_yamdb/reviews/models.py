from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель категорий произведений."""
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
        ordering = ('name', )

    def __str__(self):
        return self.name[:50]


class Genre(models.Model):
    """Модель жанров произведений."""
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
        ordering = ('name', )

    def __str__(self):
        return self.name[:50]


class Title(models.Model):
    """Модель произведений."""
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
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        verbose_name='Slug категории',
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name', )

    def __str__(self):
        return self.name[:50]


class Review(models.Model):
    """Модель отзывов к произведениям."""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            ),
        ]
        ordering = ('-pub_date', )


class Comment(models.Model):
    """Модель комментариев к отзывам к произведениям."""
    review = models.ForeignKey(
        Review,
        verbose_name='Ревью',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
