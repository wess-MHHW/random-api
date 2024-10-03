
from rest_framework import permissions

class IsHouseManagerOrNone(permissions.BasePermission):
    """Permission class that allows house manager to update only their own user. 
    For other users, only safe methods (GET) and creating new resources (POST) are permitted."""

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """ 
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_anonymous:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.profile == obj.manager
      