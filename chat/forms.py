from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

# TODO Форма для регистрации
class UserRegistrationForm(forms.ModelForm):
    # Поля из стандартной модели User
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    # Поля из нашей модели UserProfile
    email = forms.CharField(label='Еmail')

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)