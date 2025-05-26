from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status


class IsStaffOrReadOnly(BasePermission):
    """
    Allows full access only to staff users.
    - Safe (read-only) methods (GET, HEAD, OPTIONS) are allowed for any user.
    - Any other method (POST, PUT, DELETE, etc.) requires staff privileges.
    """

    def has_permission(self, request, view):
        print(request.user)
        if request.method in SAFE_METHODS:
            return True
        if bool(request.user and request.user.is_staff):
            return True
        return False


class IsAdminForDeleteOrPatchOrReadOnly(BasePermission):
    """
    Object-level permission:
    - Allows read-only methods for all users.
    - Allows DELETE only for superusers.
    - Allows PATCH/PUT for staff users.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        elif request.method == 'DELETE':
            return bool(request.user and request.user.is_superuser)

        else:
            return bool(request.user and request.user.is_staff)


class IsOwner(BasePermission):
    """
    Object-level permission:
    - Allows read-only access for all users.
    - Allows DELETE only for superusers.
    - Allows updates only for:
        - The object's owner,
        - The 'Guest' user,
        - Or a superuser.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        elif request.method == 'DELETE':
            return bool(request.user and request.user.is_superuser)

        else:
            is_owner = bool(
                request.user and (
                    request.user.id == obj.id or
                    request.user.username == 'Guest' or
                    request.user.is_superuser
                )
            )
            return is_owner
