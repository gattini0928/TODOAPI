from validate_docbr import CPF
from django.core.exceptions import ValidationError
from django.contrib.messages import constants as messages

def validate_name(name):
    if not name or len(name.split()) <= 1:
        raise ValidationError('Enter your full name')
    return name

def validate_cpf(cpf):
    cpf_obj = CPF()
    if not cpf_obj.validate(cpf):
        raise ValidationError(f'{cpf}, Invalid CPF')
    return cpf

def validate_email(email):
    domains = ['icloud', 'gmail.com', 'outlook.com', 'yahoo.com']
    domain = email.split('@')[-1]
    if domain not in domains:
        raise ValidationError('Invalid email domain')
    return email
