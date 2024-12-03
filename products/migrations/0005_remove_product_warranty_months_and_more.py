# Generated by Django 4.2.16 on 2024-11-30 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='warranty_months',
        ),
        migrations.AddField(
            model_name='product',
            name='is_best_seller',
            field=models.BooleanField(default=False, help_text='Mark this product as a best seller.'),
        ),
    ]