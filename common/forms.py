from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Пользователь")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    next = forms.CharField(widget=forms.HiddenInput(), required=False)