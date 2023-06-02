menu = [
    {"title": "Главная", "url_name": "core:index"},
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


def is_same_user(request, pk) -> bool:
    return request.user.pk == pk
