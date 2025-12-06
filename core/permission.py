from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class IsEditor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'editor']


class IsViewer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'editor', 'viewer']
