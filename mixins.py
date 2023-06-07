from copy import deepcopy

from django.contrib.auth.mixins import \
    LoginRequiredMixin as LoginRequiredMixinDjango, AccessMixin
from django.urls import reverse_lazy
from django.views.generic.base import ContextMixin

import utils


class MenuMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(kwargs=kwargs)
        if not context:
            context = dict()
        context["menu"] = deepcopy(utils.menu.copy())
        return context


class AuthMenuMixin(MenuMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(kwargs=kwargs)
        if self.request.user.is_authenticated:
            profile_menu = deepcopy(utils.profile)
            profile_menu[0]["user_pk"] = self.request.user.pk
            context["menu"] += deepcopy(profile_menu)
            context["menu"] += deepcopy(utils.authorized_menu.copy())
        else:
            context["menu"] += deepcopy(utils.unauthorized_menu.copy())
        return context


class LoginRequiredMixin(LoginRequiredMixinDjango):
    login_url = reverse_lazy("profiles:login")


class StaffOnlyMixin(AccessMixin):
    login_url = reverse_lazy("profiles:login")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
