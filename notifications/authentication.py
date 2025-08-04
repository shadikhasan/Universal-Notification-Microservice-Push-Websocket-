# notifications/authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Tenant

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Api-Key "):
            return None

        api_key = auth_header.split(" ")[1]
        try:
            tenant = Tenant.objects.get(api_key=api_key)
        except Tenant.DoesNotExist:
            raise AuthenticationFailed("Invalid API key")

        return (tenant, None)  # User object is tenant
