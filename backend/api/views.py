import json
import tempfile
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import Response, HttpResponse
from rest_framework.decorators import api_view, permission_classes

from rest_framework import viewsets, status
from rest_framework.generics import (
    get_object_or_404,
    )
from rest_framework.permissions import IsAuthenticated
from wsgiref.util import FileWrapper

from .models import Recipe, Ingredient, Tag, Purchase
from .serializers import (
    RecipeSerializer,
    IngredientSerializer,
    PurchaseSerializer,
    )
from .viewsets import ListCreateDestroyViewSet

User = get_user_model()


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, ]
    filter_fields = ['author__username', ]

    def create(self, request, *args, **kwargs):
        request_ingredients = json.loads(self.request.data.get('ingredient'))
        request_tags = json.loads(self.request.data.get('tag'))
        ingredients = []
        for request_ingredient in request_ingredients:
            ingredients.append(Ingredient.objects.get_or_create(
                name=request_ingredient.get('name'),
                amount=request_ingredient.get('amount'),
                measurement_unit=request_ingredient.get(
                    'measurement_unit'))[0]
                    )
        author = get_object_or_404(User, username=self.request.user)
        tags = Tag.objects.filter(name__in=request_tags)
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ingredient=ingredients,
                            tag=tags,
                            author=author)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        request_ingredients = self.request.data.get('ingredient')
        request_ingredients = json.loads(request_ingredients)

        request_tags = self.request.data.get('tag')
        request_tags = json.loads(request_tags)

        ingredients = []
        for request_ingredient in request_ingredients:
            ingredients.append(Ingredient.objects.get_or_create(
                name=request_ingredient.get('name'),
                amount=request_ingredient.get('amount'),
                units=request_ingredient.get('measurement_unit'))[0])
        author = get_object_or_404(User, username=self.request.user)
        tags = Tag.objects.filter(name__in=request_tags)
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer.save(ingredient=ingredients,
                        tag=tags,
                        author=author)
        return Response(serializer.data)


class FavoriteAPIView(ListCreateDestroyViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, ]
    filter_fields = ['author__username', ]

    def get_queryset(self):
        tag_list = self.request.GET.getlist('tag__name')
        if tag_list:
            queryset = Recipe.objects.filter(
                subscribers=self.request.user,
                tag__name__in=tag_list).distinct()
        else:
            queryset = Recipe.objects.filter(subscribers=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe,
                                   pk=self.request.data.get('favorite'))
        recipe.subscribers.add(self.request.user)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe,
                                   pk=self.kwargs['pk'])
        recipe.subscribers.remove(self.request.user)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class PurchaseAPIView(ListCreateDestroyViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Purchase.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe,
                                   pk=self.request.data.get('purchase'))
        serializer.save(user=self.request.user,
                        purchase=recipe)


@api_view(http_method_names=['POST'])
@permission_classes((IsAuthenticated, ))
def download_purchases(request, *args, **kwargs):
    ingredients = {}
    for item in request.data:
        for ingredient in item['purchase']['ingredient']:
            ingredient_key = (f"{ingredient['name']}"
                              f"({ingredient['measurement_unit']})")
            if ingredient_key in ingredients.keys():
                ingredients[ingredient_key] += ingredient['amount']
            else:
                ingredients[ingredient_key] = ingredient['amount']

    with tempfile.TemporaryDirectory():
        with open('file_text.txt', 'w+') as f:
            for key in ingredients.keys():
                f.write(f'{key} — {ingredients[key]}\n')

            f.seek(0)
            response = HttpResponse(
                FileWrapper(f),
                content_type='application/text charset=utf-8')
            response['Content-Disposition'] = ('attachment; '
                                               "filename='f.txt'")
            return response
