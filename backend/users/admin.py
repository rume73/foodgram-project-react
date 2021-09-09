from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import User, Follow


class UserResource(resources.ModelResource):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'password',
                  'email',)


class UserAdmin(ImportExportModelAdmin):
    search_fields = ('email', 'name',)


class FollowResource(resources.ModelResource):

    class Meta:
        model = Follow
        fields = ('id', 'user', 'author')


class FollowAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'author',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
