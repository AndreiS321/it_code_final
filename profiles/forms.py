from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from profiles import models


class NoInitialValueFileInput(forms.ClearableFileInput):
    def is_initial(self, value):
        return False


class ProfileUpdate(UserChangeForm):
    password = None
    profile_pic = forms.ImageField(initial=None,
                                   label="Аватар профиля",
                                   widget=NoInitialValueFileInput)
    description = forms.CharField(label="Сообщение",
                                  widget=forms.Textarea,
                                  required=False)

    class Meta:
        model = models.Profile
        fields = ("username", "profile_pic", "description")


class ProfileCreate(UserCreationForm):
    class Meta:
        model = models.Profile
        fields = ("username", "password1", "password2")
