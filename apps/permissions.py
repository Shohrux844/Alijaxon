from django.contrib.auth.mixins import AccessMixin


class IsOperatorRequire(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.role != 'operator':
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)