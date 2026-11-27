from django.conf import settings

from rest_framework import exceptions
from rest_framework.authentication import (
    CSRFCheck,
    TokenAuthentication,
)


class CookieTokenAuthentication(TokenAuthentication):
    """Autenticación mediante token almacenado en cookie HttpOnly."""

    def authenticate(self, request):
        nombre_cookie = settings.AUTH_COOKIE["NAME"]
        token = request.COOKIES.get(nombre_cookie)

        if not token:
            return None

        user, auth = self.authenticate_credentials(token)
        self.enforce_csrf(request)
        return user, auth

    def enforce_csrf(self, request):
        check = CSRFCheck(lambda req: None)
        check.process_request(request)
        razon = check.process_view(
            request,
            None,
            (),
            {},
        )

        if razon:
            raise exceptions.PermissionDenied(
                f"CSRF Failed: {razon}"
            )
