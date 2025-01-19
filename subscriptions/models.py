from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User

from carts.models import CartItems

class Subscription(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"), related_name="%(class)s" ,on_delete=models.CASCADE)
    items = models.ForeignKey(CartItems, verbose_name=_("items"), on_delete=models.CASCADE)
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)

    class Meta:
        db_table = 'subscriptions'
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')

    def __str__(self):
        return f"اشتراک{self.user.username}"