from django.test import TestCase
from django.core.exceptions import ValidationError
from .validators.form_validators import *
from django.contrib.auth.password_validation import validate_password

class ValidationTests(TestCase):
    def test_validate_name_success(self):
        name = 'Gabriel Gattini'
        self.assertEqual(
            validate_name(name),
            name.strip(),
            msg=f"Expected name '{name.strip()}', but got a validation error"
        )

    def test_validate_name_error(self):
        names_to_test = ['Gabriel', ' ', 'G']
        for name in names_to_test:
            with self.assertRaises(ValidationError, msg=f"Name '{name}' should raise ValidationError"):
                validate_name(name)

    def test_validate_password_success(self):
        password = 'Happy0928*'
        try:
            validate_password(password)
            print(f"Password '{password}' passed validation.")  # Debug info
        except ValidationError as e:
            print(f"Password '{password}' failed validation: {e}")
            raise

    def test_validate_password_error(self):
        invalid_passwords = ['happy0928*', 'Happy0928', 'happy', 'HAPPY', '0928', '*&&', ' ']
        for password in invalid_passwords:
            with self.assertRaises(ValidationError, msg=f"Password '{password}' should raise ValidationError"):
                validate_password(password)

    def test_validate_email_success(self):
        email = 'gabrielgattini659@gmail.com'
        try:
            validate_email(email)
            print(f"Email '{email}' passed validation.")  # Debug info
        except ValidationError as e:
            print(f"Email '{email}' failed validation: {e}")
            raise

    def test_validate_email_error(self):
        invalid_emails = ['gabrielgattini659@hotmail.com', ' ', '@gmail.com', 'gabrielgattini659@gmail']
        for email in invalid_emails:
            with self.assertRaises(ValidationError, msg=f"Email '{email}' should raise ValidationError"):
                validate_email(email)

    def test_validate_cpf_success(self):
        cpf = '03741308099'
        try:
            validate_cpf(cpf)
            print(f"CPF '{cpf}' passed validation.")  # Debug info
        except ValidationError as e:
            print(f"CPF '{cpf}' failed validation: {e}")
            raise

    def test_validate_cpf_error(self):
        invalid_cpfs = ['0374130809', '000000000000', ' ']
        for cpf in invalid_cpfs:
            with self.assertRaises(ValidationError, msg=f"CPF '{cpf}' should raise ValidationError"):
                validate_cpf(cpf)


