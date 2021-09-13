from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers

from .models import User, Follow
from api_foodgram import settings


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'is_subscribed',
            'username',
            'first_name',
            'last_name',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Follow.objects.filter(author=obj, user=user).exists()


class ShowFollowersSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, user):
        current_user = self.context.get('current_user')
        other_user = user.following.all()
        if user.is_anonymous:
            return False
        if other_user.count() == 0:
            return False
        if Follow.objects.filter(user=user, author=current_user).exists():
            return True
        return False

    def get_recipes(self, obj):
        from api.serializers import ShowRecipeAddedSerializer
        recipes = obj.recipes.all()[:settings.RECIPES_LIMIT]
        request = self.context.get('request')
        return ShowRecipeAddedSerializer(
            recipes,
            many=True,
            context={'request': request}
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class FollowSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()

    class Meta:
        model = Follow
        fields = ('user', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author'],
                message=('Вы уже подписались на этого автора.')
            )
        ]

    def validate(self, data):
        user = self.context['request'].user
        author = data.get('author')
        if user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )

        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return ShowFollowersSerializer(
            instance.author,
            context={'request': request}
        ).data
