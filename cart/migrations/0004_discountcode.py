# Generated by Django 5.1.7 on 2025-03-23 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_order_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('discount', models.SmallIntegerField(default=0)),
                ('quantity', models.SmallIntegerField(default=1)),
            ],
        ),
    ]
