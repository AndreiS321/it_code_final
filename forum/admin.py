from django.contrib import admin

from forum.models import Category, Theme, ThemeMessage

# Register your models here.
admin.site.register((Category, Theme, ThemeMessage))
