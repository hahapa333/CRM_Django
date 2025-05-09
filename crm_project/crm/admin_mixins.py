from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin

class GroupRequiredMixin(AccessMixin):
    group_required = None  # Можно передать строку или список

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return self.handle_no_permission()

        # Админ всегда имеет доступ
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Проверка групп
        required = self.group_required
        if isinstance(required, str):
            required = [required]

        if not user.groups.filter(name__in=required).exists():
            return redirect('permission_denied')

        return super().dispatch(request, *args, **kwargs)
