from django import forms
from django.utils.translation import gettext_lazy as _


class ContactUsForm(forms.Form):
    full_name = forms.CharField(label=_("نام کامل"), max_length=80)
    email = forms.EmailField(label=_("ایمیل"))
    phone_number = forms.IntegerField(label=_("شماره تلفن"))
    message = forms.CharField(label=_("پیام"), widget=forms.Textarea())
    