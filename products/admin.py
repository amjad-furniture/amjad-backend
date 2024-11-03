from django.contrib import admin

from products.models import Material, Product, ProductImage

# Register your models here.

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Material)
