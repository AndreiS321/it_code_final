from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView

import utils
from forum import models, forms
from mixins import AuthMenuMixin, StaffOnlyMixin, \
    LoginRequiredMixin


# Create your views here.
class CategoriesView(AuthMenuMixin, ListView):
    model = models.Category
    template_name = "forum/categories.html"
    extra_context = {"title": "Категории"}

    def get_queryset(self):
        return self.model.objects.annotate(
            themes_count=Count("themes"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(kwargs=kwargs)
        context["user"] = self.request.user
        return context


class CategoryCreate(StaffOnlyMixin, LoginRequiredMixin,
                     AuthMenuMixin, CreateView):
    model = models.Category
    template_name = "forum/category_create.html"
    fields = ("name",)
    success_url = reverse_lazy("forum:categories")
    extra_context = {"title": "Создание категории"}

    def post(self, request, *args, **kwargs):
        category_name = request.POST.get("name")
        self.model.objects.create(creator_id=self.request.user.pk,
                                  name=category_name)
        return redirect(reverse("forum:categories"))


class CategoryDelete(StaffOnlyMixin, LoginRequiredMixin,
                     AuthMenuMixin, DeleteView):
    model = models.Category
    template_name = "forum/category_delete.html"
    success_url = reverse_lazy("forum:categories")
    extra_context = {"title": "Удаление категории"}


class ThemesView(AuthMenuMixin, ListView):
    model = models.Theme
    template_name = "forum/themes.html"

    def get_queryset(self):
        pk = self.kwargs.get("category_pk")
        return self.model.objects.filter(category__pk=pk).annotate(
            msg_count=Count("messages"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(kwargs=kwargs)

        category = get_object_or_404(
            models.Category,
            pk=self.kwargs.get("category_pk"))
        context["category"] = category
        context["title"] = f"Категория {category.name}"

        context["user"] = self.request.user
        return context


class ThemeCreate(LoginRequiredMixin, AuthMenuMixin,
                  CreateView):
    model = models.Theme
    template_name = "forum/theme_create.html"
    fields = ("name",)
    extra_context = {"title": "Создание темы"}

    def get_success_url(self):
        return reverse("forum:themes",
                       kwargs={"pk": self.kwargs.get("category_pk")})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(kwargs=kwargs)
        context["category_pk"] = self.kwargs.get("category_pk")
        return context

    def post(self, request, *args, **kwargs):
        category_pk = self.kwargs.get("category_pk")
        theme_name = request.POST.get("name")
        self.model.objects.create(category_id=category_pk,
                                  creator_id=self.request.user.pk,
                                  name=theme_name)
        return redirect(reverse("forum:themes",
                                kwargs={"category_pk": category_pk}))


class ThemeDelete(LoginRequiredMixin, AuthMenuMixin,
                  DeleteView):
    model = models.Theme
    template_name = "forum/theme_delete.html"
    extra_context = {"title": "Удаление темы"}

    def dispatch(self, request, *args, **kwargs):
        creator = get_object_or_404(models.Theme,
                                    pk=self.kwargs.get("pk")).creator
        is_same_user = utils.is_same_user(request.user, creator)
        if not (self.request.user.is_staff or is_same_user):
            return utils.handle_no_permission(
                reverse("forum:themes",
                        kwargs={"category_pk": self.kwargs.get("category_pk")
                                }))
        return super().dispatch(request, args=args, kwargs=kwargs)

    def get_success_url(self):
        return reverse("forum:themes",
                       kwargs={"category_pk": self.kwargs.get("category_pk")})


class ThemeMessagesView(AuthMenuMixin, ListView):
    paginate_by = 4
    model = models.ThemeMessage
    template_name = "forum/theme.html"

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return self.model.objects.filter(theme__pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(kwargs=kwargs)

        theme = get_object_or_404(models.Theme,
                                  pk=self.kwargs.get("pk"))
        context["theme"] = theme
        context["title"] = f"Тема {theme.name}"

        context["is_staff"] = self.request.user.is_staff
        context["user"] = self.request.user

        context["form"] = forms.ThemeMessageForm(
            initial={"theme_pk": theme.pk})
        return context


class ThemeMessageCreate(LoginRequiredMixin, View):
    def post(self,
             request,
             *args,
             **kwargs):
        text = request.POST.get("text")
        theme_pk = int(request.POST.get("theme_pk"))
        models.ThemeMessage.objects.create(
            theme_id=theme_pk, text=text, from_user_id=self.request.user.pk)
        return redirect(
            f'{reverse("forum:theme", kwargs={"pk": theme_pk})}'
            f'?page=last')


class ThemeMessageDelete(LoginRequiredMixin, AuthMenuMixin,
                         DeleteView):
    model = models.ThemeMessage
    template_name = "forum/msg_delete.html"
    extra_context = {"title": "Удаление сообщения"}

    def dispatch(self, request, *args, **kwargs):
        from_user = self.get_object().from_user
        is_same_user = utils.is_same_user(request.user, from_user)

        if not (self.request.user.is_staff or is_same_user):
            raise PermissionDenied()

        return super().dispatch(request, args=args, kwargs=kwargs)

    def get_success_url(self):
        return reverse("forum:theme",
                       kwargs={
                           "pk": self.kwargs.get("theme_pk")
                       }) + "?page=last"
