from django.shortcuts import render
from django.views import View

from mixins import AuthMenuMixin


class IndexView(AuthMenuMixin, View):
    template_name = "core/index.html"

    def get(self, request):
        context = self.get_user_context_data()
        return render(request, self.template_name, context=context)
