from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Recipe, Ingredient


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

    def subscribers_count(self, obj):
        return obj.subscribers.all().count()
    subscribers_count.short_description = 'Количество сохранений'


class IngredientResource(resources.ModelResource):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'amount', 'measurement_unit')


class IngredientAdmin(ImportExportModelAdmin):
    resource_class = IngredientResource
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
