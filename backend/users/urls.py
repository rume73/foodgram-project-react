from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, UserView


router = DefaultRouter()
router.register('users', CustomUserViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/me/', UserView.as_view(), name='me'),
    path('', include(router.urls)),
]
