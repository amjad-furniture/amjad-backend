from django.contrib import admin

from products.models import Product, ProductImage

admin.site.register(ProductImage)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'is_best_seller', 'price', 'stock')
    list_filter = ('is_active', 'category', 'is_best_seller')
    search_fields = ('name', 'sku', 'description')
    actions = ['make_active', 'make_inactive']

    @admin.action(description="Activate selected products")
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} products were activated.")

    @admin.action(description="Deactivate selected products")
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} products were deactivated.")
