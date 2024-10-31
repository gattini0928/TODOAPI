from django import forms
from django.core.exceptions import ValidationError
from .validators.form_validators import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

class SignUpForm(forms.Form):
    name = forms.CharField(max_length=150, validators=[validate_name], help_text='Enter your full name')
    cpf = forms.CharField(max_length=15, validators=[validate_cpf], help_text='Enter a valid CPF')
    email = forms.EmailField(max_length=250, validators=[validate_email], help_text='Enter a valid e-mail')
    password = forms.CharField(widget=forms.PasswordInput(), validators=[validate_password], help_text="Enter a strong password.")

