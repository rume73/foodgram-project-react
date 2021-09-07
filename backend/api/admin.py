from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Recipe, Ingredient, Tag


class RecipeResource(resources.ModelResource):

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'description', 'cooking_time',
                  'ingredients', 'tags', 'subscribers', 'pub_date')


class RecipeAdmin(ImportExportModelAdmin):
    resource_class = RecipeResource
    list_display = ('pk', 'author', 'image', 'name', 'description',
                    'cooking_time', 'ingredients', 'tags', 'subscribers',
                    'pub_date')
    search_fields = ('name',)
    list_filter = ('pub_date',) #пока не точно
    empty_value_display = '-пусто-'


class IngredientResource(resources.ModelResource):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'amount', 'measurement_unit')


class IngredientAdmin(ImportExportModelAdmin):
    resource_class = IngredientResource
    list_display = ('pk', 'name', 'amount', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class TagResource(resources.ModelResource):

    class Meta:
        model = Tag
        fields = ('pk', 'name', 'color', 'slug')


class TagAdmin(ImportExportModelAdmin):
    resource_class = TagResource
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)