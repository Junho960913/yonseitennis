from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from user.models import User
from django import forms

class CustomCsUserChangeForm(UserChangeForm):
    password = None
    nickname = forms.CharField(label='닉네임', widget=forms.TextInput(
        attrs={'class': 'form-control', 'maxlength': '24'}),
    )

    class Meta:
        model = User()
        fields = ['nickname']
