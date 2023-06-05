from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from profiles.models import Profile

menu = [
    {"title": "Главная", "url_name": "core:index"},
    {"title": "Форум", "url_name": "forum:categories"},
]

unauthorized_menu = [
    {"title": "Войти", "url_name": "profiles:login"},
    {"title": "Регистрация", "url_name": "profiles:registration"},
]

authorized_menu = [
    {"title": "Выйти", "url_name": "profiles:logout"},
]

profile = [
    {"title": "Профиль", "url_name": "profiles:profile", "user_pk": None},
]


def is_same_user(user1: Profile | int, user2: Profile | int) -> bool:
    user1 = user1.pk if isinstance(user1, Profile) else user1
    user2 = user2.pk if isinstance(user2, Profile) else user2
    return user1 == user2


def handle_no_permission(redirect_to: str) -> HttpResponseRedirect:
    return redirect(redirect_to)
