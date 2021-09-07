from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager, UserRole


class User(AbstractUser):
    username = models.CharField(
        'Уникальный юзернейм',
        max_length=150,
        unique=True
        )
    password = models.CharField('Пароль', max_length=150)
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True
        )
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    role = models.CharField(
        'Статус пользователя',
        max_length=30,
        choices=UserRole.choices,
        default=UserRole.USER
        )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    objects = UserManager()

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
