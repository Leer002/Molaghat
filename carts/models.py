import jdatetime

from django.db import models
from django.utils.translation import gettext_lazy as _ 

from users.models import User
from places.models import Place

class CartItems(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    place = models.ForeignKey(Place, verbose_name=_("place"), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("quantity"), default=0)
    is_purchased = models.BooleanField(_("is purchased"), default=False)
    date_added = models.DateTimeField(_("date added"), auto_now_add=True)

    class Meta:
        db_table = _("cart")
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def __str__(self):
        return f"تعداد: {self.quantity}, در: {self.place}"
    
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = _("user_info")
        verbose_name = _("User_info")
        verbose_name_plural = _("User_infos")


class CartItemInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("quantity"), default=0)
    price = models.IntegerField(_("price"), blank=True, null=True)
    event_date = models.DateField(_("event date"), blank=True, null=True)
    city = models.CharField(_("city"), max_length=80, blank=True, null=True)
    category = models.CharField(_("category"), max_length=80, null=True)
    place_name = models.CharField(_("place"), max_length=60, blank=True, null=True)
    event = models.CharField(_("title"), max_length=100, blank=True, null=True)
    updated_time = models.DateTimeField(_("updated time"), auto_now=True)

    class Meta:
        db_table = _("cart_info")
        verbose_name = _("Cart_info")
        verbose_name_plural = _("Cart_infos")
    
    def get_event_date_shamsi(self):
        return jdatetime.date.fromgregorian(date=self.event_date)

