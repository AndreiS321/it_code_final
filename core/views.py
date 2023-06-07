from django.shortcuts import render
from django.views import View

from mixins import AuthMenuMixin


class IndexView(AuthMenuMixin, View):
    template_name = "core/index.html"
    extra_context = {"title": "Главная"}

    def get(self, request, **kwargs):
        context = self.get_context_data(kwargs=kwargs)
        return render(request, self.template_name, context=context)
