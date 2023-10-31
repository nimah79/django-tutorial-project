from typing import Optional, Tuple, TypeVar

from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.tokens import Token

from spotify.models import JwtIdentifier

AuthUser = TypeVar("AuthUser", AbstractBaseUser, TokenUser)


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        user, validated_token = super().authenticate(request)

        try:
            identifier = validated_token['identifier']
        except KeyError:
            raise InvalidToken(_("Token contained no identifier"))
        if not JwtIdentifier.objects.filter(identifier=identifier).exists():
            raise InvalidToken(_("Invalid identifier"), code="invalid_identifier")

        return user, validated_token
