from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from .models import Recipe, User


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class TagAndAuthorFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author']
