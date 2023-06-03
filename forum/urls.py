from django.urls import path

from forum import views

app_name = 'forum'

urlpatterns = [
    path("", views.CategoriesView.as_view(), name="categories"),
]