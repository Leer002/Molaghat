from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _ 

class UsernameValidator(RegexValidator):
    regex = r'^[a-zA-Z][a-zA-Z0-9_.]+$'
    message = _('Enter a valid username starting with a-z. '
                'This value may contain only letters, numbers and underscore characters.'),
    code = 'invalid_username'

class PhoneNumberValidator(RegexValidator):
    regex = r'^98(9[0-3,9]\d{8}|[1-9]\d{9})$'
    message = 'Phone number must be a VALID 12 digits like 98xxxxxxxxxx'
    code = 'invalid_phone_number'

validate_username = UsernameValidator()
validate_phone_number = PhoneNumberValidator()