from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _ 

class UsernameValidator(RegexValidator):
    regex = r'^[a-zA-Z][a-zA-Z0-9_.]+$'
    message = _('یک نام کاربری معتبر که با a-z شروع می شود وارد کنید. این مقدار ممکن است فقط شامل حروف، اعداد و کاراکترهای زیرخط باشد.'),
    code = 'invalid_username'

class PhoneNumberValidator(RegexValidator):
    regex = r'^98(9[0-3,9]\d{8}|[1-9]\d{9})$'
    message = 'شماره تلفن باید 12 رقمی معتبر مانند 98xxxxxxxxxx باشد.'
    code = 'invalid_phone_number'

validate_username = UsernameValidator()
validate_phone_number = PhoneNumberValidator()