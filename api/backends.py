import jwt

from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        is_token_invalid = (not auth_header or
                            len(auth_header) == 1 or
                            len(auth_header) > 2)

        if is_token_invalid:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(token)

    def _authenticate_credentials(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(pk=payload['id'])

        except jwt.exceptions.DecodeError:
            msg = "Authentication failed. could not decode token"
            raise exceptions.AuthenticationFailed(msg)

        except User.DoesNotExist:
            msg = "No user matching the token provided"
            raise exceptions.AuthenticationFailed(msg)

        else:
            return (user, token)
