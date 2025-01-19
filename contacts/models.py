from django.db import models
from django.utils.translation import gettext_lazy as _ 

from utils.validators import validate_phone_number

class ContactUs(models.Model):
    full_name = models.CharField(_("full name"), max_length=80, null=True)
    email = models.EmailField(_("email"), null=True)
    phone_number = models.BigIntegerField(_("phone number"), validators=[validate_phone_number], null=True)
    message = models.TextField(_("message"), null=True)
    time = models.DateTimeField(_("time"), auto_now_add=True)
    # پیام توسط ادمین خوانده شده یا نه
    read = models.BooleanField(_("read"), default=False)

    class Meta:
        db_table = _("contact")
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")