from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def group_required(group_name):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # Check if the user belongs to the specified group
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied  # Deny access if the user is not in the required group
        return _wrapped_view
    return decorator
