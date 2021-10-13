from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)



class RegisterForm(forms.Form):
    name = forms.CharField(max_length=500)
    email = forms.EmailField()
    image = forms.FileField()
    password = forms.CharField(widget=forms.PasswordInput)
