from functools import wraps
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    """
    Decorator factory: allow access only to authenticated users whose role is in *roles.
    Unauthenticated users are redirected to login.
    Authenticated users without matching role get 403 PermissionDenied.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if user.is_superuser or getattr(user, "role", None) in roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped
    return decorator


def accountant_required(view_func):
    """Shortcut decorator for accountant-only views."""
    return role_required('ACCOUNTANT')(view_func)


def director_required(view_func):
    """Shortcut decorator for director-only views."""
    return role_required('DIRECTOR')(view_func)