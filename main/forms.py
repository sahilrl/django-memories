from inspect import formatargspec
from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label='Your email', max_length=100)