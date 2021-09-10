from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     Purchase, Tag)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'


class IngredientResource(resources.ModelResource):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'amount', 'measurement_unit')


class IngredientAdmin(ImportExportModelAdmin):
    resource_class = IngredientResource
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class IngredientsInline(admin.TabularInline):
    model = Ingredient


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ingredient',
        'recipe',
        'amount'
    )
    empty_value_display = '-пусто-'


class RecipeResource(resources.ModelResource):

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'description', 'cooking_time',
                  'ingredients', 'tags', 'subscribers', 'pub_date')


class RecipeAdmin(ImportExportModelAdmin):
    resource_class = RecipeResource
    list_display = ('pk', 'name', 'author',)
    search_fields = ('name', 'author', 'tags')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'

    def is_favorited(self, obj):
        return obj.favorites.count()

    def ingredients(self, obj):
        return list(obj.ingredients.all())
    ingredients.short_description = 'Ингредиенты'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    empty_value_display = '-пусто-'


class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'purchase',
    )
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
