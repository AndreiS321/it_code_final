from copy import deepcopy

from django.contrib.auth.mixins import LoginRequiredMixin as LoginRequiredMixinDjango
from django.urls import reverse_lazy

import utils


class MenuMixin:
    def get_user_context_data(self, context: dict = None, *, object_list=None, **kwargs):
        if not context:
            context = dict()
        context["menu"] = deepcopy(utils.menu.copy())
        return context


class AuthMenuMixin(MenuMixin):
    def get_user_context_data(self, context: dict = None, *, object_list=None, **kwargs):
        context = super().get_user_context_data(context, kwargs=kwargs)
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
