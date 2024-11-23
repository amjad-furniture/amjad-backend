# Generated by Django 4.2.16 on 2024-11-23 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_product_materials_product_fabric_material_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Set to False to hide the product from being displayed.'),
        ),
    ]
