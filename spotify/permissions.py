from rest_framework import permissions


class BlacklistPermission(permissions.BasePermission):
    message = "Your IP is blocked."

    def has_permission(self, request, view):
        ip_address = request.META["REMOTE_ADDR"]

        return ip_address not in ("127.0.0.1",)
