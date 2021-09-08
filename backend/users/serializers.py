from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
import django.contrib.auth.password_validation as validators
from rest_framework import serializers
from django.core import exceptions

from users.models import User


class ChangePasswordSerializer(serializers.ModelSerializer):
    model = User
    old_password = serializers.CharField(required=True, min_length=8)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password_again = serializers.CharField(required=True, min_length=8)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'new_password_again')

    def validate(self, data):
        password = data.get('new_password')
        errors = dict()
        try:
            validators.validate_password(password=password)
        except exceptions.ValidationError as e:
            errors['new_password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super(ChangePasswordSerializer, self).validate(data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email',
                  'role']
        extra_kwargs = {
            'password': {'required': True},
            'email': {'required': True}
        }


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ConfCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        user = get_object_or_404(User, email=data['email'])
        if not default_token_generator.check_token(user,
                                                   data['confirmation_code']):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'})
        return data
