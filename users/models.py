import jdatetime
import random

from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _ 
from django.core.mail import send_mail

from utils.validators import validate_username, validate_phone_number
  
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, email=None, phone_number=None, is_staff=False, is_superuser=False, **extra_fields):
        if not username:
            raise ValueError(".قسمت نام کاربری باید تنظیم شود")
        if not email:
            raise ValueError(".فیلد ایمیل باید تنظیم شود")
        
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            phone_number=phone_number,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=True,
            date_joined=timezone.now(),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password, email, phone_number, **extra_fields):
        user =  self.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=phone_number,
            is_staff=True,
            is_superuser=True,
            **extra_fields
        )
        UserProfile.objects.create(user=user)
        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), unique=True, max_length=30, validators=[validate_username], help_text=_('30 کاراکتر یا کمتر که با یک حرف شروع می شود. فقط حروف، اعداد و خط زیر خط.'), 
                    error_messages={'unique':_("کاربری با این نام کاربری از قبل وجود دارد."),})
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    email = models.EmailField(_("email"), unique=True, blank=True, null=True)
    phone_number = models.BigIntegerField(_("phone number"), null=True, blank=True, validators=[validate_phone_number], error_messages={'unique': _("کاربری با آن شماره تلفن از قبل وجود دارد.")}, help_text="با 98 شروع کن")

    is_staff = models.BooleanField(_("is staff"), default=False)
    is_active = models.BooleanField(_("is active"), default=True)

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_seen = models.DateTimeField(_('last seen date'), null=True)

    objects = UserManager()

    REQUIRED_FIELDS = ["email", "phone_number"]
    USERNAME_FIELD = "username"

    class Meta:
        db_table = 'users'
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name
    
    def short_name(self):
        return self.first_name
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
    
    @property
    def is_loggedin_user(self):
        return self.phone_number is not None or self.email is not None
    
    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == "":
            self.email = None
        super().save(*args, **kwargs)
         
class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("user"), on_delete=models.CASCADE)
    nick_name = models.CharField(_("nick name"), max_length=50, blank=True, null=True)
    birthdate = models.DateField(_("birthdate"), blank=True, null=True)
    avatar = models.ImageField(_("avatar"), blank=True, null=True, upload_to="profiles/")

    class Meta:
        db_table = "profiles"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def get_event_date_shamsi(self):
           return jdatetime.date.fromgregorian(date=self.birthdate)
    
    @property
    def get_first_name(self):
        return self.user.first_name
    
    @property
    def get_last_name(self):
        return self.user.last_name
    
    def get_nickname(self):
        return self.nick_name if self.nick_name else self.user.first_name
        
