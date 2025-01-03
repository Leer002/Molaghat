from django.db import models
from django.utils.translation import gettext_lazy as _ 
from django.core.exceptions import ValidationError

class Category(models.Model):
    parent = models.ForeignKey("self", verbose_name=_("parent"), on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(_("title"), max_length=60, unique=True)
    is_enable = models.BooleanField(_("is enable"), default=False)
    description = models.TextField(_("description"), blank=True)
    image = models.ImageField(_("image"), blank=True, upload_to="categories/")
    updated_time = models.DateTimeField(_("updated time"), auto_now=True)
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)

    class Meta:
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    

class Place(models.Model):
    place = models.CharField(_("place"), max_length=60)
    event = models.CharField(_("title"), max_length=100)
    is_enable = models.BooleanField(_("is enable"), default=False)
    category = models.ForeignKey(Category, verbose_name=_("category"), on_delete=models.SET_NULL, null=True)
    image = models.ImageField(_("image"), upload_to="places/")
    description = models.TextField(_("description"), blank=True)
    address = models.TextField(_("address"))
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=3)
    capacity = models.PositiveIntegerField(_("capacity"))
    updated_time = models.DateTimeField(_("updated time"), auto_now=True)
    event_date = models.DateTimeField(_("event date"))

    class Meta:
        db_table = "places"
        verbose_name = "Place"
        verbose_name_plural = "Places"

    def __str__(self):
        return self.event
    
    def clean(self):
        if self.capacity == 0:
            raise ValidationError('Value cannot be zero.')