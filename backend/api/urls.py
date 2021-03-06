from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from .views import (
    RecipeViewSet,
    IngredientViewSet,
    TagViewSet,
    FavoriteAPIView,
    PurchaseAPIView,
    DownloadShoppingCart)


router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')


urlpatterns = [
    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view(),
         name='download_shopping_cart'),
    path('', include(router.urls)),
    path('recipes/<int:recipe_id>/shopping_cart/', PurchaseAPIView.as_view(),
         name='add_recipe_to_shopping_cart'),
    path('recipes/<int:recipe_id>/favorite/', FavoriteAPIView.as_view(),
         name='add_recipe_to_favorite'),
]
