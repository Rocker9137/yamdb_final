from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import validate_year

User = get_user_model()

NUM_OF_LETTERS = 15


class Category(models.Model):
    """Модель категории произведений."""
    name = models.CharField(
        verbose_name='Категории (типы) произведений',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Уникальная строка идентификатор категории',
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name[:NUM_OF_LETTERS]


class Genre(models.Model):
    """Модель жанра произведений."""
    name = models.CharField(
        verbose_name='Категории жанров',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Уникальная строка идентификатор жанра',
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name[:NUM_OF_LETTERS]


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        verbose_name='Название',
        max_length=300
    )
    year = models.IntegerField(
        verbose_name='Дата выхода',
        validators=[validate_year]
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name[:NUM_OF_LETTERS]


class Review(models.Model):
    """Модель отзыва на произведение."""
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва'
    )
    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзыв',
        blank=False,
        help_text='Произведение, к которому относится комментарий',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        blank=False,
    )
    score = models.IntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        help_text='Введдите оценку'
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='only_one_review'
            )
        ]

    def __str__(self) -> str:
        return self.text[:NUM_OF_LETTERS]


class Comment(models.Model):
    """Модель комментария на произведение."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        blank=False,
        help_text='Отзыв, к которому относится комментарий',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        blank=False,
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        ordering = ['pub_date']

    def __str__(self) -> str:
        return self.text[:NUM_OF_LETTERS]
