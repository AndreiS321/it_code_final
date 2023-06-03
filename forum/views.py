from django.views.generic import ListView

from forum import models
from mixins import AuthMenuMixin


# Create your views here.
class CategoriesView(AuthMenuMixin, ListView):
    model = models.Category
    template_name = "forum/categories.html"

