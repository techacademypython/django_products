from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control"
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control"
        }
    ))


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class":"form-control"
        }
    ))

    class Meta:
        model = User
        fields = [
            "username"
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            )
        }
