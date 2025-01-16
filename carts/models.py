from django.db import models
from django.utils.translation import gettext_lazy as _ 

from users.models import User
from places.models import Place

class CartItems(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    place = models.ForeignKey(Place, verbose_name=_("place"), on_delete=models.CASCADE)
    date_added = models.DateTimeField(_("date added"), auto_now_add=True)
    quantity = models.PositiveIntegerField(_("quantity"), default=0)

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

    
