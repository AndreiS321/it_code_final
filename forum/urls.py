from django.urls import path

from forum import views

app_name = 'forum'

urlpatterns = [
    path("", views.CategoriesView.as_view(),
         name="categories"),
    path("category/create", views.CategoryCreate.as_view(),
         name="category_create"),
    path("category/delete/<int:pk>", views.CategoryDelete.as_view(),
         name="category_delete"),

    path("themes/<int:category_pk>", views.ThemesView.as_view(),
         name="themes"),
    path("theme/<int:pk>", views.ThemeMessagesView.as_view(),
         name="theme"),
    path("theme/create/<int:category_pk>", views.ThemeCreate.as_view(),
         name="theme_create"),
    path("theme/delete/<int:category_pk>/<int:pk>",
         views.ThemeDelete.as_view(),
         name="theme_delete"),

    path("message/create/", views.ThemeMessageCreate.as_view(),
         name="create_message"),
]
