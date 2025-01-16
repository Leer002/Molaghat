from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _ 

from .models import User, UserProfile

class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields":("username", "password")}),
        (_("Personal info"), {"fields":("first_name", "last_name", "phone_number", "email")}),
        (_("Permissions"), {"fields":("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields":("last_login", "date_joined")})
    )
    add_fieldsets = (
        (None, {"classes":("wide",), "fields":("username", "phone_number", "password1", "password2")})
    )
    list_display = ("username", "phone_number", "email", "is_staff")
    search_fields = ["username__exact", "phone_number"]
    ordering = ("-id",)

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates =  super().get_search_results(request, queryset, search_term)

        try:
            search_term_int = int(search_term)
        except ValueError:
            pass
        else:
            queryset |= queryset.model.objects.filter(phone_number=search_term_int)

        return queryset, may_have_duplicates

@admin.register(UserProfile)
class MyUserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "nick_name", "birthdate")
    search_fields = ("user__username",)
    ordering = ("-id",)

admin.site.unregister(Group)
admin.site.register(User, MyUserAdmin)

        