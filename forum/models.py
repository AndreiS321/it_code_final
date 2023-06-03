from django.conf import settings
from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField("название категории", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}:{self.created_at}:{self.changed_at}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ("created_at",)


class Theme(models.Model):
    name = models.CharField("название темы", max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category}:{self.name}"

    class Meta:
        verbose_name = "тема"
        verbose_name_plural = "темы"
        ordering = ("created_at",)


class Message(models.Model):
    text = models.TextField("текст сообщения")
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"


class ThemeMessage(Message):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="messages")
