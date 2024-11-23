from django.contrib import admin

from categories.models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')