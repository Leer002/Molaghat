from django.db import models
from django.utils.translation import gettext_lazy as _ 

from utils.validators import validate_phone_number

from carts.models import CartItemInfo

class Gateway(models.Model):
    title = models.CharField(_("title"), max_length=40)
    description = models.TextField(_('description'), blank=True)
    avatar = models.ImageField(_('avatar'), blank=True, upload_to='gateways/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)

    class Meta:
        db_table = 'gateways'
        verbose_name = _('Gateway')
        verbose_name_plural = _('Gateways')

class Payment(models.Model):
    STATUS_PAID = 10
    STATUS_CANCELED = 30
    STATUS_CHOICES = (
        (STATUS_PAID, _('Paid')),
        (STATUS_CANCELED, _('User Canceled'))
    )
    user = models.ForeignKey('users.User', verbose_name=_('user'), related_name='%(class)s', on_delete=models.CASCADE)
    gateway = models.ForeignKey(Gateway, verbose_name=_('gateway'), related_name='%(class)s', on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItemInfo, verbose_name=_('items'), blank=True)
    price = models.PositiveIntegerField(_('price'), default=0)
    status = models.PositiveSmallIntegerField(_('status'), choices=STATUS_CHOICES, default=30)
    device_uuid = models.CharField(_('device uuid'), max_length=40, blank=True)
    token = models.CharField(_('token'), max_length=36, blank=True)
    phone_number = models.BigIntegerField(_('phone number'), validators=[validate_phone_number], help_text=_(".با 98 شماره تلفن را شروع کنید"))
    consumed_code = models.PositiveIntegerField(_('consumed code'), null=True)
    created_time = models.DateTimeField(_('creation time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('modification time'), auto_now=True)

    class Meta:
        db_table = 'payments'
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')