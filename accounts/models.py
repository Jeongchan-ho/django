from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignupForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        db_table = 'my_accounts'
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')