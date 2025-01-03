from django.contrib import admin

from .models import Category, Place

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ["place", "event", "is_enable", "get_categories", "event_date", "price"]
    search_fields = ["event", "place", "category"]
    list_filter = ["is_enable"]

    def get_categories(self, obj):
        return obj.category.title if obj.category else "No Category"

    get_categories.short_description = "category"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["parent", "title", "is_enable"]
    search_fields = ["title"]
    list_filter = ["is_enable", "parent"]