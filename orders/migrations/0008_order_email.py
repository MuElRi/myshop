# Generated by Django 4.2.16 on 2024-12-05 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_order_city_order_postal_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default='eldar00319@mail.ru', max_length=254),
            preserve_default=False,
        ),
    ]