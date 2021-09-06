from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager, UserRole


class User(AbstractUser):
    username = models.CharField(verbose_name='Уникальный юзернейм',
                                max_length=150, unique=True)
    password = models.TextField(verbose_name='Пароль', max_length=150)
    email = models.EmailField(verbose_name='Адрес электронной почты',
                              max_length=254, unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=150)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150)
    role = models.CharField(verbose_name='Статус пользователя',
                            max_length=30, choices=UserRole.choices,
                            default=UserRole.USER)

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
