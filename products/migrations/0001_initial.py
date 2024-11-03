# Generated by Django 4.2.16 on 2024-11-03 09:47

from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Material Name')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Product Name')),
                ('sku', models.CharField(blank=True, editable=False, max_length=12, unique=True, verbose_name='SKU')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=100, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('color', models.CharField(blank=True, max_length=50, null=True, verbose_name='Color')),
                ('width_cm', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, verbose_name='Width (cm)')),
                ('height_cm', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, verbose_name='Height (cm)')),
                ('depth_cm', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, verbose_name='Depth (cm)')),
                ('stock', models.IntegerField(blank=True, null=True, verbose_name='Stock')),
                ('country_of_origin', models.CharField(blank=True, max_length=100, null=True, verbose_name='Country of Origin')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='categories.category', verbose_name='Category')),
                ('materials', models.ManyToManyField(related_name='products', to='products.material', verbose_name='Materials')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=products.models.product_image_upload_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
            ],
        ),
    ]