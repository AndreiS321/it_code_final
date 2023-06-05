from django import forms

from forum import models


class ThemeMessageForm(forms.Form):
    text = forms.CharField(label="Сообщение", widget=forms.Textarea)
    theme_pk = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = models.ThemeMessage
        fields = ("text",)
