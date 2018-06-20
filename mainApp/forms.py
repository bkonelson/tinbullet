from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    #username = forms.CharField(max_length=254)
    #password1 = forms.CharField(min_length=8, max_length=254)
    #password2 = forms.CharField(min_length=8, max_length=254)
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )