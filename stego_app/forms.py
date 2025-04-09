from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class EncryptForm(forms.Form):
    file = forms.FileField()
    message = forms.CharField(max_length=500)
    secret_code = forms.CharField(max_length=100)

class DecryptForm(forms.Form):
    file = forms.FileField()
    secret_code = forms.CharField(max_length=100)
