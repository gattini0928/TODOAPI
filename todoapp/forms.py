from django import forms
from django.core.exceptions import ValidationError
from .validators.form_validators import *
from django.contrib.auth.password_validation import validate_password

class SignupForm(forms.Form):
    name = forms.CharField(max_length=150, validators=[validate_name])
    cpf = forms.CharField(max_length=15, validators=[validate_cpf])
    email = forms.EmailField(max_length=250)
    password = forms.CharField(widget=forms.PasswordInput(), validators=[validate_password])
