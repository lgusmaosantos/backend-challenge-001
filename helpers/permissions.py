"""
Custom permissions for general use
"""
###
# Libraries
###
from rest_framework import permissions

###
# Permission classes
###
class ObjectPermissionIsAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """A simple permission class that inherits from
    `IsAuthenticatedOrReadOnly` and ensures that only
    an object's owner can change or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # For safe methods (e.g.: `GET`),
        # access to an object is granted
        if request.method in permissions.SAFE_METHODS:
            return True

        # For all other methods only the object's owner
        # is allowed
        return obj.author == request.user
