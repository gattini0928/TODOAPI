import string
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def __init__(self):
        self.min_length = 8
        self.requirements = {
            'uppercase': True,
            'lowercase': True,
            'digits': True,
            'special': True,
        }

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("Your password must not contain at least %(max_length) of characters."),
                code="password_too_short",
                params={"min_length": self.min_length},
            )
        
        if self.requirements['uppercase'] and not any(c.isupper() for c in password):
            raise ValidationError(
                _("Your password must be have at least  one uppercase letter"),
                code="password_no_uppercase",
            )
        
        if self.requirements['lowercase'] and not any(c.islower() for c in password):
            raise ValidationError(
                _("Your password must be have at least  one lowercasse letter"),
                code="password_no_lowercase",
            )
        
        if self.requirements['digits'] and not any(c.isdigit() for c in password):
            raise ValidationError(
                _("Your password must be have at least one digit"),
                code="password_no_digit",
            )
        
        if self.requirements['special'] and not any(c in string.punctuation for c in password):
            raise ValidationError(
                _("Your password must be have at least one special character"),
                code="password_no_special",
            )

    def get_help_text(self):
        requirements = []
        if self.requirements['uppercase']:
            requirements.append(_('At least one capital letter'))
        if self.requirements['lowercase']:
            requirements.append(_('At least one lowercase letter'))
        if self.requirements['digits']:
            requirements.append(_("At least one digit"))
        if self.requirements['special']:
            requirements.append(_("At least one special character"))
        
        return _("Your password must have one of this requirements: ") + ", ".join(requirements)