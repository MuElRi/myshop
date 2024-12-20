# Generated by Django 4.2.16 on 2024-12-04 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_apartment_number_order_house_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(default='Ufa', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.CharField(default='465024', max_length=20),
            preserve_default=False,
        ),
    ]
