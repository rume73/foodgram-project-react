from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        )
    # amount = 
    # measurement_unit = 


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        )
    color = models.CharField(
        max_length=7,
        verbose_name='Цветовой HEX-код',
        )
    slug = models.SlugField(
        "Часть URL адреса тега",
        unique=True,
        max_length=200,
        help_text="Укажите адрес для страницы тэга. "
                  "Используйте только латиницу, цифры, дефисы "
                  "и знаки подчёркивания"
        )


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name='Автор рецепта',
        null=True
        )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        )
    image = models.ImageField(
        upload_to="static/images",
        verbose_name="Изображение",
        null=True,
        blank=True,
        help_text="Загрузите изображение"
        )
    description = models.TextField(
        "Описание",
        help_text="Введите описание рецепта"
        )
    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления (в минутах)",
        validators=[MinValueValidator(1), MaxValueValidator(1440)]
        )
    ingredients = []
    tags = []
    subscribers = models.ManyToManyField(
        User,
        default=None,
        related_name='subscribers',
        blank=True,
        verbose_name='Сохранившие'
        )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
        )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name
