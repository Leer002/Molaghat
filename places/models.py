import jdatetime

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
    place_name = models.CharField(_("place"), max_length=60)
    event = models.CharField(_("title"), max_length=100)
    is_enable = models.BooleanField(_("is enable"), default=False)
    category = models.ForeignKey(Category, verbose_name=_("category"), on_delete=models.SET_NULL, null=True)
    image = models.ImageField(_("image"), upload_to="places/")
    description = models.TextField(_("description"), blank=True)
    address = models.TextField(_("address"))
    area = models.CharField(_("area"), max_length=60, blank=True, null=True)
    city = models.CharField(_("city"), max_length=80)
    price = models.IntegerField(_("price"))
    capacity = models.PositiveIntegerField(_("capacity"))
    event_date = models.DateField(_("event date"), max_length=50)
    event_time = models.CharField(_("event time"), max_length=5, blank=True, null=True)
    updated_time = models.DateTimeField(_("updated time"), auto_now=True)

    class Meta:
        db_table = "places"
        verbose_name = "Place"
        verbose_name_plural = "Places"

    def __str__(self):
        return self.event
    
    def clean(self):
        if self.capacity == 0:
            raise ValidationError('Value cannot be zero.')
    
    def get_event_date_shamsi(self):
           """تاریخ ایونت را به شمسی تبدیل کند."""
           return jdatetime.date.fromgregorian(date=self.event_date)
        
class File(models.Model):
    place = models.ForeignKey("Place", verbose_name=_("place"), on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=50)
    file = models.FileField(_("file"), upload_to="files/%Y/%M/%D/")
    is_enable = models.BooleanField(_('is enable'), default=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)

    class Meta:
        db_table = 'files'
        verbose_name = _('file')
        verbose_name_plural = _('files')

    def __str__(self):
        return self.title