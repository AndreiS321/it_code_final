from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from profiles.models import Profile

# Register your models here.
admin.site.register(Profile, UserAdmin)
