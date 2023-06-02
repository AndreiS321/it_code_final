from django.contrib.auth import logout
from django.contrib.auth.views import LoginView as LoginViewDjango
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView

import utils
from profiles import models, forms
from profiles.mixins import LoginRequiredMixin, AuthMenuMixin


class ProfileDetail(AuthMenuMixin, DetailView):
    model = models.Profile
    template_name = "profiles/profile.html"


    def get_context_data(self, **kwargs):
        context = self.get_user_context_data(context=super().get_context_data())
        if utils.is_same_user(self.request, context["object"].pk):
            context["is_same_user"] = True
        return context


class ProfileUpdate(AuthMenuMixin, LoginRequiredMixin, UpdateView):
    model = models.Profile
    form_class = forms.ProfileUpdate
    template_name = "profiles/update.html"

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if not utils.is_same_user(request, obj.pk):
            raise PermissionDenied("Нет доступа")
        return super().get(request, args, kwargs)

    def get_success_url(self):
        return reverse("profiles:profile", kwargs={"pk": self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = self.get_user_context_data(context=super().get_context_data())
        return context


class RegisterView(AuthMenuMixin, CreateView):
    model = models.Profile
    form_class = forms.ProfileCreate
    template_name = "profiles/registration.html"
    success_url = reverse_lazy("profiles:login")

    def get_context_data(self, **kwargs):
        context = self.get_user_context_data(context=super().get_context_data())
        return context


class LoginView(AuthMenuMixin, LoginViewDjango):
    template_name = "profiles/login.html"

    def get_success_url(self):
        return reverse("core:index")

    def get_context_data(self, **kwargs):
        context = self.get_user_context_data(context=super().get_context_data())
        return context


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("core:index"))


