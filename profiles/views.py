from django.contrib.auth import logout
from django.contrib.auth.views import LoginView as LoginViewDjango, \
    PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

import utils
from forum import models as forum_models
from mixins import LoginRequiredMixin, AuthMenuMixin
from profiles import models, forms


class ProfileDetail(AuthMenuMixin, DetailView):
    model = models.Profile
    template_name = "profiles/profile.html"
    extra_context = {"title": "Профиль"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.get_object()
        context["latest_messages"] = forum_models.ThemeMessage.objects.filter(
            from_user__pk=user.pk).order_by("-created_at")[:3]
        context["is_same_user"] = utils.is_same_user(self.request.user, user)
        return context


class ProfileUpdate(AuthMenuMixin, LoginRequiredMixin,
                    UpdateView):
    model = models.Profile
    form_class = forms.ProfileUpdate
    template_name = "profiles/update.html"
    extra_context = {"title": "Редактирование профиля"}

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not utils.is_same_user(request.user, obj.pk):
            raise PermissionDenied()
        return super().dispatch(request, args=args, kwargs=kwargs)

    def get_success_url(self):
        return reverse("profiles:profile",
                       kwargs={"pk": self.request.user.pk})


class ProfileDelete(AuthMenuMixin, LoginRequiredMixin,
                    DeleteView):
    model = models.Profile
    template_name = "profiles/delete.html"
    extra_context = {"title": "Удаление профиля"}

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not utils.is_same_user(request.user, obj.pk):
            raise PermissionDenied()
        return super().dispatch(request, args=args, kwargs=kwargs)

    def get_success_url(self):
        return reverse("core:index")


class ChangePasswordView(AuthMenuMixin, LoginRequiredMixin,
                         PasswordChangeView):
    extra_context = {"title": "Смена пароля"}
    template_name = "profiles/change_password.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not utils.is_same_user(request.user, obj.pk):
            raise PermissionDenied()
        self.object = obj
        return super().dispatch(request, args=args, kwargs=kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(kwargs=kwargs)
        context["object"] = self.object
        return context

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(models.Profile, pk=pk)

    def get_success_url(self):
        return reverse("profiles:profile",
                       kwargs={"pk": self.request.user.pk})


class RegisterView(AuthMenuMixin, CreateView):
    model = models.Profile
    form_class = forms.ProfileCreate
    template_name = "profiles/registration.html"
    success_url = reverse_lazy("profiles:login")
    extra_context = {"title": "Регистрация"}


class LoginView(AuthMenuMixin, LoginViewDjango):
    template_name = "profiles/login.html"
    extra_context = {"title": "Вход"}

    def get_success_url(self):
        return reverse("core:index")


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect(reverse("core:index"))
