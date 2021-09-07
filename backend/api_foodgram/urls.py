from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/', include('api.urls')),
    path('api/', include('users.urls')),
    path('docs/', TemplateView.as_view(template_name='redoc.html'),
         name='docs'),
    path('docs/openapi-schema.yml',
         TemplateView.as_view(template_name='openapi-schema.yml'),
                              name='openapi-schema'),
]
