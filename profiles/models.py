from django.contrib.auth.models import AbstractUser
from django.db import models


def get_pic_url(self, filename):
    return f"profiles/{self.pk}/profile_pic/{filename}"


class Profile(AbstractUser):
    profile_pic = models.ImageField("аватар профиля", upload_to=get_pic_url, default="defaults/images/noimage.png")

    description = models.TextField("обо мне")

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"
