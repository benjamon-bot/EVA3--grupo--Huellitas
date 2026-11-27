from django.conf import settings
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .autenticacion import CookieTokenAuthentication


def _poner_cookie(response, token_key):
    configuracion = settings.AUTH_COOKIE
    response.set_cookie(
        configuracion["NAME"],
        token_key,
        max_age=configuracion["MAX_AGE"],
        path=configuracion["PATH"],
        httponly=True,
        secure=configuracion["SECURE"],
        samesite=configuracion["SAMESITE"],
    )


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"csrfToken": get_token(request)})


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthTokenSerializer(
            data=request.data,
            context={"request": request},
        )

        if not serializer.is_valid():
            return Response(
                {"detail": "Usuario o contraseña incorrectos."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        response = Response(
            {"username": user.username},
            status=status.HTTP_200_OK,
        )
        _poner_cookie(response, token.key)
        return response


class MeView(APIView):
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"username": request.user.username})


class LogoutView(APIView):
    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        response = Response(status=status.HTTP_204_NO_CONTENT)
        configuracion = settings.AUTH_COOKIE
        response.delete_cookie(
            configuracion["NAME"],
            path=configuracion["PATH"],
            samesite=configuracion["SAMESITE"],
        )
        return response
