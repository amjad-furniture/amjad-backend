import random
import string
import re
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from categories.models import Category


class ArabicSlugify:
    """Custom slugify class for Arabic and English text"""
    
    @staticmethod
    def slugify(text):
        # Replace spaces with hyphens and keep Arabic, English letters, numbers, or hyphens
        text = re.sub(r'\s+', '-', text.strip())
        text = re.sub(r'[^\u0600-\u06FF\w\-]', '', text)
        return text.strip('-')


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Category")
    name = models.CharField(unique=True, max_length=100, verbose_name="Product Name")
    sku = models.CharField(max_length=12, unique=True, blank=True, editable=False, verbose_name="SKU")
    slug = models.SlugField(max_length=100, unique=True, blank=True, allow_unicode=True, verbose_name="Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    color = models.CharField(max_length=50, verbose_name="Color", blank=True, null=True)
    length_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Length (cm)")
    width_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Width (cm)")
    height_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Height (cm)")
    depth_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Depth (cm)")
    stock = models.IntegerField(null=True, blank=True, verbose_name="Stock")
    country_of_origin = models.CharField(max_length=100, blank=True, null=True, verbose_name="Country of Origin")
    product_video = models.FileField(upload_to='products-videos/', blank=True, null=True, verbose_name="Product Video")
    wood_material = models.CharField(max_length=255, blank=True, null=True, verbose_name="خامة الخشب")
    fabric_material = models.CharField(max_length=255, blank=True, null=True, verbose_name="خامة القماش")
    upholstery_material = models.CharField(max_length=255, blank=True, null=True, verbose_name="خامة التنجيد")
    warranty_months = models.PositiveIntegerField(blank=True, null=True, verbose_name="عدد شهور الضمان")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @staticmethod
    def generate_sku():
        """Generate a unique 12-character SKU with uppercase letters and numbers."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

    def generate_slug(self):
        """Generate a unique slug for the product name."""
        base_slug = ArabicSlugify.slugify(self.name)
        slug = base_slug
        existing_slugs = list(Product.objects.filter(slug__startswith=base_slug).values_list('slug', flat=True))

        if slug not in existing_slugs:
            return slug

        # Generate a unique slug by appending a number
        counter = 1
        while slug in existing_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def clean(self):
        """Model validation for custom constraints."""
        errors = {}
        if self.price <= 0:
            errors['price'] = "Price must be positive."
        if self.stock is not None and self.stock < 0:
            errors['stock'] = "Stock cannot be negative."
        if self.width_cm is not None and self.width_cm <= 0:
            errors['width_cm'] = "Width must be a positive number."
        if self.height_cm is not None and self.height_cm <= 0:
            errors['height_cm'] = "Height must be a positive number."
        if self.depth_cm is not None and self.depth_cm <= 0:
            errors['depth_cm'] = "Depth must be a positive number."
        
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Ensure slug and SKU are set appropriately on save."""
        if not self.slug:
            self.slug = self.generate_slug()
        
        if not self.sku:
            self.sku = self.generate_sku()
            while Product.objects.filter(sku=self.sku).exists():
                self.sku = self.generate_sku()
        
        super().save(*args, **kwargs)


@receiver(pre_save, sender=Product)
def product_pre_save(sender, instance, *args, **kwargs):
    """Signal to set slug and SKU before saving if they are empty."""
    if not instance.slug:
        instance.slug = instance.generate_slug()
    if not instance.sku:
        unique_sku = instance.generate_sku()
        while Product.objects.filter(sku=unique_sku).exists():
            unique_sku = instance.generate_sku()
        instance.sku = unique_sku


def product_image_upload_path(instance, filename):
    """Generate dynamic upload path for product images."""
    return f'products-images/{instance.product.id or "temp"}/{filename}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"
