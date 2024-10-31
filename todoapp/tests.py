from django.test import TestCase
from django.core.exceptions import ValidationError
from .validators.form_validators import *
from django.contrib.auth.password_validation import validate_password

class ValidationTests(TestCase):
    def test_validate_name_success(self):
        name = 'Gabriel Gattini'
        self.assertEqual(validate_name(name), name.strip())

    def test_validate_name_error(self):
        with self.assertRaises(ValidationError):
            validate_name('Gabriel')

        with self.assertRaises(ValidationError):
            validate_name(' ')

        with self.assertRaises(ValidationError):
            validate_name('G')

    def test_validate_password_success(self):
        password = 'Happy0928*'
        self.assertEqual(validate_password(password))

    def test_validate_password_error(self):
        with self.assertRaises(ValidationError):
            validate_password('happy0928*')

        with self.assertRaises(ValidationError):
            validate_password('Happy0928')

        with self.assertRaises(ValidationError):
            validate_password('happy')
        
        with self.assertRaises(ValidationError):
            validate_password('HAPPY')

        with self.assertRaises(ValidationError):
            validate_password('0928')

        with self.assertRaises(ValidationError):
            validate_password('*&&')

        with self.assertRaises(ValidationError):
            validate_password(' ')


    def test_validate_email_success(self):
        email = 'gabrielgattini659@gmail.com'
        self.assertEqual(validate_email(email))

    def test_validate_email_error(self):
        with self.assertRaises(ValidationError):
            validate_email('gabrielgattini659@hotmail.com')

        with self.assertRaises(ValidationError):
            validate_email(' ')

        with self.assertRaises(ValidationError):
            validate_email('@gmail.com')

        with self.assertRaises(ValidationError):
            validate_email('gabrielgattini659@gmail')

    
    def test_validate_cpf_success(self):
        cpf = '03741308099'
        self.assertEqual(validate_cpf(cpf))

    def test_validate_cpf_error(self):
        with self.assertRaises(ValidationError):
            validate_cpf('0374130809')

        with self.assertRaises(ValidationError):
            validate_cpf('000000000000')

        with self.assertRaises(ValidationError):
            validate_cpf(' ')
