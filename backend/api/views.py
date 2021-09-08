import json
import tempfile
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import Response

from rest_framework import viewsets, status, mixins
from rest_framework.generics import (
    get_object_or_404,
    ListCreateAPIView,
    DestroyAPIView
    )
from rest_framework.permissions import IsAuthenticated
from wsgiref.util import FileWrapper

from users.permissions import IsAdminOrAuthorOrReadOnly, IsAdminOrReadOnly
from .models import Recipe, Ingredient, Tag, Purchase, Follow
from users.serializers import UserSerializer
from .serializers import (
    RecipeSerializer,
    IngredientSerializer,
    PurchaseSerializer,
    FollowSerializer
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
    filter_backends = [DjangoFilterBackend,]
    filter_fields = ['author__username',]

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
                units=request_ingredient.get('units'))[0])
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


class FollowListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    model = Follow
    


class FollowDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    model = Follow
    queryset = Follow.objects.all()


class PurchaseAPIView(ListCreateDestroyViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        queryset = Purchase.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):

        recipe = get_object_or_404(Recipe,
                                   pk=self.request.data.get('purchase'))

        serializer.save(user=self.request.user,
                        purchase=recipe)
