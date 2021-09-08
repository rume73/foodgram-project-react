from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField('Название ингредиента', max_length=200)
    amount = models.PositiveIntegerField(
        'Количество',
        default=1,
        validators=[MinValueValidator(1), ]
    )
    measurement_unit = models.CharField('Единицы измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('Тег', max_length=200,)
    color = models.CharField('Цветовой HEX-код', max_length=7)
    slug = models.SlugField(
        "Часть URL адреса тега",
        unique=True,
        max_length=200,
        help_text="Укажите адрес для страницы тэга. "
                  "Используйте только латиницу, цифры, дефисы "
                  "и знаки подчёркивания"
        )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name='Автор рецепта',
        null=True
        )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        )
    image = models.ImageField(
        upload_to='static/images',
        verbose_name='Изображение',
        null=True,
        blank=True,
        help_text='Загрузите изображение'
        )
    description = models.TextField(
        'Описание',
        help_text='Введите описание рецепта'
        )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления (в минутах)',
        validators=[MinValueValidator(1), MaxValueValidator(1440)]
        )
    ingredients = models.ManyToManyField(
        Ingredient,
        default=None,
        related_name='ingredient',
        blank=False,
        verbose_name='Ингредиент',
        )
    tags = models.ManyToManyField(
        Tag,
        related_name='tag',
        blank=False,
        default='завтрак',
        verbose_name='Тег'
        )
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


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
        )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        ordering = ['-id']
        unique_together = ('user', 'author')

    def __str__(self):
        return f'пользователь {self.user} подписан на {self.author}'


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer',
        verbose_name='Пользователь'
        )
    purchase = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchase',
        verbose_name='Покупка'
        )

    class Meta:
        verbose_name = 'покупка'
        verbose_name_plural = 'покупки'

    def __str__(self):
        return f'пользователь {self.user} покупает {self.purchase}'
