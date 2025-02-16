from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedForWriteMethods(BasePermission):
    """
    Permite acesso livre para GET, mas exige autenticação para PUT, POST e DELETE.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # Métodos seguros: GET, HEAD, OPTIONS
            return True  # GET é permitido sem autenticação
        return request.user and request.user.is_authenticated  # Exige autenticação para escrita
