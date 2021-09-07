from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Нужны права администратора'

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin)


class IsAdmin(permissions.BasePermission):
    message = 'Нужны права администратора'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsModerator(permissions.BasePermission):
    message = 'Нужны права модератора'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author == request.user


class IsSuperuser(permissions.BasePermission):
    message = 'Нужны права администратора Django'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            if (request.method == 'POST' and request.user.is_authenticated
                    or request.user.is_staff or request.user.is_admin
                    or request.user.is_moderator
                    or obj.author == request.user):
                return True
        elif request.method in permissions.SAFE_METHODS:
            return True
