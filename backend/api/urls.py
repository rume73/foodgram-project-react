from django.conf.urls import include
from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers

from .views import (
    RecipeViewSet,
    IngredientViewSet,
    FollowListCreateAPIView,
    FollowDestroyAPIView,
    FavoriteAPIView,
    PurchaseAPIView,
    download_purchases
    )


router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes/(?P<recipe_id>\d+)/favorite',
                FavoriteAPIView, basename='favorite'),
router.register(r'recipes/download_shopping_cart/', PurchaseAPIView,
                basename='download_shopping_cart')


urlpatterns = [
    path('', include(router.urls),),
    path('users/', include('users.urls')),
    path('subscriptions/', FollowListCreateAPIView.as_view()),
    path('subscriptions/<int:pk>/', FollowDestroyAPIView.as_view()),
    path('download/', download_purchases),
    path('docs/', TemplateView.as_view(template_name='redoc.html'),
         name='docs'),
    path('docs/openapi-schema.yml',
         TemplateView.as_view(template_name='openapi-schema.yml'),
         name='openapi-schema'),
]
