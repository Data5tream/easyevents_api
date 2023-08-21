from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners or admins of an object to view it
    """
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user or request.user.groups.has(name="admins")
