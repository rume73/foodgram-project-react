from django.urls import include, path

from .views import FollowAPIView, ListFollowView, UserView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('<int:author_id>/subscribe/', FollowAPIView.as_view(),
         name='subscribe'),
    path('subscriptions/', ListFollowView.as_view(),
         name='subscriptions'),
    path('me/', UserView.as_view(), name='me'),
    path('', include('djoser.urls')),
]
