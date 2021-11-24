from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        """Check if the user has permission to write

        Parameters
        ----------
        reauest
            user request

        Returns
        -------
        boolean
            True if user is admin
        """
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.is_staff
        )
