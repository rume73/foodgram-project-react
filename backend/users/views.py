from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Follow
from .serializers import (FollowSerializer, ShowFollowersSerializer,
                          UserSerializer)

User = get_user_model()


class UserView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user


class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, author_id):
        user = request.user
        data = {
            'user': user.id,
            'author': author_id
        }
        serializer = FollowSerializer(data=data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, author_id):
        user = request.user
        author = get_object_or_404(User, id=author_id)
        obj = get_object_or_404(Follow, user=user, author=author)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListFollowView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ShowFollowersSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)
