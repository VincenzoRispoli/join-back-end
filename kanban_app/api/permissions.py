from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        is_staff = bool(request.user and request.user.is_staff)
        return is_staff or request.method in SAFE_METHODS
    
    
class IsAdminForDeleteOrPatchOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
           return True
        elif request.method == 'DELETE':
           return bool(request.user and request.user.is_superuser)
        else :
            return bool(request.user and request.user.is_staff)
    
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user)
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'DELETE':
            return bool(request.user.id and request.user.is_superuser)
        else:
            is_owner = bool(request.user and request.user.id == obj.user.id or request.user.username == 'Guest')
            return is_owner
    
    