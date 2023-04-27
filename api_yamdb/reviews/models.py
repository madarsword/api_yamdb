from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.contrib.auth import get_user_model


User = get_user_model()  # удалить и заменить на
                         # Саниного абстракт юзера


class Review(models.Model):

    title = models.ForeignKey(
        Title,  # нужен мердж по Теминому пул реквесту
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(  # выглядит как костыль. Подумайте тоже плиз
                1,
                message='Оценка должна быть больше 1',
            ),
            MaxValueValidator(  # аналогично
                10,
                message='Оценка должна быть меньше 10',
            ),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации отзыва',
    )
