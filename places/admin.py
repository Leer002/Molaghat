from django.contrib import admin

from .models import Category, Place, File

class FileInlineAdmin(admin.TabularInline):
    model = File
    fields = ["title", "file", "is_enable"]
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["parent", "title", "is_enable"]
    search_fields = ["title"]
    list_filter = ["is_enable", "parent"]

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ["place_name", "event", "is_enable", "get_categories", "event_date", "price"]
    search_fields = ["event", "place_name", "category"]
    list_filter = ["is_enable"]
    inlines = [FileInlineAdmin]

    def get_categories(self, obj):
        return obj.category.title if obj.category else "No Category"

    get_categories.short_description = "category"

