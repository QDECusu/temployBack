from rest_framework import permissions
from rest_framework.permissions import IsAdminUser

class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderators").exists()

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user or request.user.is_admin

class IsOwnerOrAdminOrMod(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or IsAdminUser or request.user.groups.filter(name="Moderators").exists()

# class IsAdminOrMod(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return IsAdminUser or request.user.groups.filter(name="Moderators").exists()

def IsAdminOrMod(request):
    return IsAdmin(request) or request.user.groups.filter(name="Moderators").exists()

def IsAdmin(request):
    return request.user.is_staff