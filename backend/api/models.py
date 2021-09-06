from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название блюда',
    )
    image = models.ImageField(upload_to="api/", verbose_name="Картинка",
                              help_text="Загрузите картинку")
    text = models.TextField("Текст", help_text="Введите описание рецепта")
    cooking_time = models.IntegerField("Время приготовления (в минутах)",
                                       auto_now_add=True)
    ingredients = []
    tags = []

    class Meta:
        ordering = ('name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name
