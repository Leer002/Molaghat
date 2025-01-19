from django import forms
from django.utils.translation import gettext_lazy as _

from django import forms
from .models import ContactUs

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'phone_number', 'message']
        labels = {
            'full_name': _("نام کامل"),
            'email': _("ایمیل"),
            'phone_number': _("شماره تلفن"),
            'message': _("پیام"),
        }
