# Generated by Django 5.1.7 on 2025-03-19 21:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_informationalproduct_alter_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='informationalproduct',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='informational_products', to='product.product'),
        ),
    ]
