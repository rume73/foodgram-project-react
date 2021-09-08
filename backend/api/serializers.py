from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Recipe, Ingredient, Tag, Purchase, Follow
from users.serializers import UserSerializer
from api_foodgram.settings import BASE_URL

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    ingredients = IngredientSerializer(many=True, read_only=True)
    image = serializers.ImageField(
        max_length=None,
        required=True,
        allow_empty_file=False,
        use_url=True,
    )
    image_url = serializers.SerializerMethodField('get_image_url')
    subscribers = UserSerializer(many=True, read_only=True,)

    class Meta:
        fields = '__all__'
        model = Recipe

    def get_image_url(self, recipe):
        request = self.context.get('request')
        if request:
            image_url = recipe.image.url

            return f'{BASE_URL}{image_url}'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate(self, attrs):
        if self.context.get('request').method == 'POST':
            author_username = self.context.get('request').data.get('author')
            author = get_object_or_404(User, username=author_username)
            user = self.context.get('request').user
            if user == author:
                raise serializers.ValidationError(
                    'Нельзя подписаться на самого себя')
            if Follow.objects.filter(user=user, author=author):
                raise serializers.ValidationError(
                    'Вы уже подписаны на этого автора')
        return attrs

    class Meta:
        fields = '__all__'
        model = Follow


class PurchaseSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    purchase = RecipeSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Purchase
